from argparse import ArgumentParser
import logging

import boto3

# Set log level to INFO and suppress botocore logs up to CRITICAL
logging.basicConfig()
logging.getLogger('botocore').setLevel(logging.CRITICAL)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

EC2 = boto3.resource('ec2')

def manage_ec2_instances(tag_value, action):
    instances = EC2.instances.filter(
        Filters=[{'Name': 'tag:TAG', 'Values': [f"{tag_value}"]}] #ADAPT THE TAG TO YOUR NEED
    )
    for instance in instances:
        name = [tag for tag in instance.tags if tag['Key'] == 'Name'][0]['Value']
        if action == 'start':
            r = instance.start()
            response_key = 'StartingInstances'
        elif action == 'stop':
            r = instance.stop()
            response_key = 'StoppingInstances'
        previous_state = r[response_key][0]['PreviousState']
        current_state = r[response_key][0]['CurrentState']
        LOGGER.info(f"Instance ({instance.id}|{name}), previous: {previous_state} | current: {current_state}")

def lambda_handler(event, context):
    tag_value = os.environ['TAG_VALUE']
    action = os.environ['ACTION']
    manage_ec2_instances(tag_value, action)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('tag_value', type=str, help='EC2 instances holding lambda-start-stop set to this value will receive the action')
    parser.add_argument('action', help='{start|stop}', choices=('start', 'stop'))
    args = parser.parse_args()

    manage_ec2_instances(args.tag_value, args.action)
