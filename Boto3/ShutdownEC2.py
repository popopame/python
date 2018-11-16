import boto3

ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(Filters=[{'Name': 'tag:group', 'Values': ['docker_host']}])

for instance in instances:
    print(instance.id)

