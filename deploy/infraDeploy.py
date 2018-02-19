#!/usr/bin/python
import boto3
import time
import json

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
    StackName='HollowApp-RDS',
    TemplateURL='https://s3.amazonaws.com/theithollow-cfn/HollowApp/RDS.json',
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
status('HollowApp-RDS')
varPass = {'RDS':'HollowApp-RDS'}

response = client.create_stack(
    StackName='HollowApp-EC2-LB',
    TemplateURL='https://s3.amazonaws.com/theithollow-cfn/HollowApp/EC2-hollowapp.json',
    Parameters=[
        {
            'ParameterKey': "Environment",
            'ParameterValue': "Sandbox"
        }
    ]
)

status('HollowApp-EC2-LB')
varPass['EC2'] = 'HollowApp-EC2-LB'

#export variables to a file for use later on in the pipeline
with open('variables.json', 'w') as outfile:
    json.dump(varPass, outfile)

with open('variables.json', 'r') as infile:
    print infile.read()
