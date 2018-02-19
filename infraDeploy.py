#!/usr/bin/python
import boto3
import time

client = boto3.client('cloudformation', region_name='us-east-1')

#functions
def status(stack):
    while True:
        stackStatus = client.describe_stacks(StackName=stack)
        status=(stackStatus['Stacks'][0]['StackStatus'])
        print "{}'s current status is {}.".format(stack, status)
        if (status == 'CREATE_FAILED') or (status == 'CREATE_COMPLETE') or (status == 'ROLLBACK_IN_PROGRESS') or (status == 'ROLLBACK_FAILED') or (status == 'ROLLBACK_COMPLETE'):
            break
        time.sleep(10)
    if status != 'CREATE_COMPLETE':
        exit()


response = client.create_stack(
    StackName='RDS',
    TemplateURL='file://CloudFormation/RDS.json',
    Parameters=[
        {
            'ParameterKey': "Availability",
            'ParameterValue': "False"
        },
        {
            'ParameterKey': "AZ",
            'ParameterValue': "us-east-1a"
        }
    ]
)
status('RDS')

response = client.create_stack(
    StackName='HollowEC2App',
    TemplateURL='file://CloudFormation/ec2-HollowApp.json',
    Parameters=[
        {
            'ParameterKey': "Environment",
            'ParameterValue': "Sandbox"
        },
        {
            'ParameterKey': "AccountShortName",
            'ParameterValue': "sbx"
        },
        {
            'ParameterKey': "VPCFunction",
            'ParameterValue': "sbx"
        },
        {
            'ParameterKey': "Web1Subnet",
            'ParameterValue': "subnet-a693d1c2"
        },
        {
            'ParameterKey': "Web2Subnet",
            'ParameterValue': "subnet-5d68e872"
        },
        {
            'ParameterKey': "InstanceSecurityGroups",
            'ParameterValue': "sg-131d9964"
        },
        {
            'ParameterKey': "VPC",
            'ParameterValue': "vpc-8c9ac2f4"
        },
        {
            'ParameterKey': "EC2KeyPair",
            'ParameterValue': "SBX-ed2-keypair"
        }
    ]
)

status('HollowEC2App')
