import boto3

group=str(input("Please enter the group you want to act on : "))
state= str(input("Please enter the state wanted with these instance : start , stop or terminate : "))


ec2 = boto3.resource('ec2')

if state == "start" :
    ec2.instances.filter(Filters=[{'Name': 'tag:group', 'Values': [group]}]).start()
elif state == "stop":
    ec2.instances.filter(Filters=[{'Name': 'tag:group', 'Values': [group]}]).stop()
elif state == "terminate":
    ec2.instances.filter(Filters=[{'Name': 'tag:group', 'Values': [group]}]).terminate()




