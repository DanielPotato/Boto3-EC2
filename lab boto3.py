import boto3

aws_access_key_id = 'ASIA27PHHZ5EHGLPK64P'
aws_secret_access_key = 'O+dBYnRatY0EPhq1tYnx1n3dFDOI5YQxi8CHfZCF'
aws_session_token = 'FwoGZXIvYXdzEPH//////////wEaDNWbcOYpMepr3ZvwEiLDAXcIWWGddYofq5wQT4Dc7zgijw8oyHAZSKcQedHWYzoU+kOQdki9OrEHm9abYtwyBC1ic7US+RTCq+Au6RY8oTnQ15fE7PR5sQY/EoG9wJSXjTZYKCxR+CiBlF+FPcGWArjfyMoibP9qeeOuqGXfaq+jjCtEvPpUWUttqg4bhQ18UBkmN3QP2nZewS6wQmkS8qc1cTUwVMgz6el0ZvVt1tFQOm2UlNqVL7SiCQVsaBsHOor2/zFhEsb7FINFJUQ9IG2r1CjL9cGqBjItq0SQXwLzHG9DaDz9qM8CcdkbL0X9TtB0v4iidNrjryEX3Ba5OEHWdzL/oM4T'

# Set the AWS region
region = "us-west-2"

# Specify the region when creating the EC2 client
ec2 = boto3.client('ec2',
                      region_name=region,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      aws_session_token=aws_session_token)


# Step 1: Retrieve the AMI ID
az_response = ec2.describe_availability_zones()
availability_zone = az_response['AvailabilityZones'][0]['ZoneName']
region = availability_zone[:-1]  # Extract region from availability zone

ssm = boto3.client('ssm', region_name=region)
ami_response = ssm.get_parameters(Names=['/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'])
ami = ami_response['Parameters'][0]['Value']

print(f"Using AMI: {ami}")

# Step 2: Retrieve the subnet ID
subnet_response = ec2.describe_subnets(Filters=[{'Name': 'tag:Name', 'Values': ['Public Subnet']}])
subnet_id = subnet_response['Subnets'][0]['SubnetId']

print(f"Using Subnet ID: {subnet_id}")

# Step 3: Retrieve the security group ID
sg_response = ec2.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': ['WebSecurityGroup']}])
security_group_id = sg_response['SecurityGroups'][0]['GroupId']

print(f"Using Security Group ID: {security_group_id}")

# Step 4: Download user data script
import urllib.request

urllib.request.urlretrieve('https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-100-RESTRT-1-23732/171-lab-JAWS-create-ec2/s3/UserData.txt', 'UserData.txt')

# Step 5: Launch the instance
response = ec2.run_instances(
    ImageId=ami,
    InstanceType='t3.micro',
    KeyName='your_key_pair_name',
    UserData=open('UserData.txt').read(),
    SubnetId=subnet_id,
    SecurityGroupIds=[security_group_id],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'Web Server'}
            ]
        }
    ]
)

instance_id = response['Instances'][0]['InstanceId']

print(f"Instance ID: {instance_id}")

# Wait for the instance to be ready
waiter = ec2.get_waiter('instance_running')
waiter.wait(InstanceIds=[instance_id])

# Step 7: Test the web server
describe_response = ec2.describe_instances(InstanceIds=[instance_id])
public_dns = describe_response['Reservations'][0]['Instances'][0]['PublicDnsName']

print(f"Public DNS: {public_dns}")

# You can now test the web server by opening the public DNS in a web browser