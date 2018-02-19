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
        time.sleep(5)
    if status != 'CREATE_COMPLETE':
        exit()

response = client.create_stack(
    StackName='HollowEC2App',
    TemplateURL='https://s3.amazonaws.com/theithollow-cfn/common/ec2-HollowApp.json',
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
            'ParameterValue': "subnet-d8dd5985"
        },
        {
            'ParameterKey': "Web2Subnet",
            'ParameterValue': "subnet-8990d2ed"
        },
        {
            'ParameterKey': "InstanceSecurityGroups",
            'ParameterValue': "sg-a499c1d3"
        },
        {
            'ParameterKey': "VPC",
            'ParameterValue': "vpc-4b9ac233"
        },
        {
            'ParameterKey': "EC2KeyPair",
            'ParameterValue': "sec-ec2-keypair"
        }
    ]
)

status('HollowEC2App')

response = client.describe_stack_resource(
    StackName='HollowEC2App',
    LogicalResourceId='Web1'
)
print(response)
