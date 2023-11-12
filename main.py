import boto3
import pprint

# Replace the following with your actual access key, secret key, and session token
aws_access_key_id = 'ASIA27PHHZ5EHGLPK64P'
aws_secret_access_key = 'O+dBYnRatY0EPhq1tYnx1n3dFDOI5YQxi8CHfZCF'
aws_session_token = 'FwoGZXIvYXdzEPH//////////wEaDNWbcOYpMepr3ZvwEiLDAXcIWWGddYofq5wQT4Dc7zgijw8oyHAZSKcQedHWYzoU+kOQdki9OrEHm9abYtwyBC1ic7US+RTCq+Au6RY8oTnQ15fE7PR5sQY/EoG9wJSXjTZYKCxR+CiBlF+FPcGWArjfyMoibP9qeeOuqGXfaq+jjCtEvPpUWUttqg4bhQ18UBkmN3QP2nZewS6wQmkS8qc1cTUwVMgz6el0ZvVt1tFQOm2UlNqVL7SiCQVsaBsHOor2/zFhEsb7FINFJUQ9IG2r1CjL9cGqBjItq0SQXwLzHG9DaDz9qM8CcdkbL0X9TtB0v4iidNrjryEX3Ba5OEHWdzL/oM4T'

# Specify the region when creating the EC2 client
client = boto3.client('ec2',
                      region_name='us-west-2',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      aws_session_token=aws_session_token)

my_ec2 = client.describe_instances()

pprint.pprint(my_ec2['Reservations'])