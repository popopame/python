import boto3

ec2 = boto3.resource('ec2')
vpc = ec2.create_default_vpc(CidrBlock='10.1.0.0/16')
subnet =vpc.create_subnet(CidrBlock='10.1.1.0/24')

ec2.create_instances(ImageId='ami-03291866', MinCount=1, MaxCount=5)