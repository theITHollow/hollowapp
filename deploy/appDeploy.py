#!/usr/bin/python
import boto3
import time
import json
import sys, os, subprocess

profile = 'sandbox'

session = boto3.Session(profile_name=profile)
client = session.client('cloudformation')
ec2client = session.client('ec2')
rdsclient = session.client('rds')

#Read the Variables File Output by the InfraDeploy Stage
json_data=open('variables.json').read()
data = json.loads(json_data)
#print(data)

#Print the results of the variables file
#print(data['EC2'])
#print(data['RDS'])

#Wanted to use this for the StackNames but this doesn't allow an expression
EC2stack = data['EC2']
RDSstack = data['RDS']

RDSresponse = client.describe_stack_resources(
    StackName="HollowApp-RDS",
    LogicalResourceId="MyDB"
)

#Get the PhysicalResourceId of the RDS datbase from the Cloudformation StackId
RDSID = RDSresponse['StackResources'][0]['PhysicalResourceId']

database = rdsclient.describe_db_instances(
    DBInstanceIdentifier=RDSID
)

#Get the RDS Instance Endpoint from the CloudFormation StackName
RDSendpoint = database['DBInstances'][0]['Endpoint']['Address']

response1 = client.describe_stack_resources(
    StackName='HollowApp-EC2-LB',
    LogicalResourceId = "HollowApp1EC2"
)
#print(response1)

response2 = client.describe_stack_resources(
    StackName=EC2stack,
    LogicalResourceId = "HollowApp2EC2"
)
#print(response2)

#Get the PhysicalResourceId from the CloudFormation Stack
EC2ID1 = response1['StackResources'][0]['PhysicalResourceId']
EC2ID2 = response2['StackResources'][0]['PhysicalResourceId']

ec2instance1 = ec2client.describe_instances(
    InstanceIds = [EC2ID1]
)

ec2instance2 = ec2client.describe_instances(
    InstanceIds = [EC2ID2]
)

EC2IP1 = ec2instance1['Reservations'][0]['Instances'][0]['PublicIpAddress']
EC2IP2 = ec2instance2['Reservations'][0]['Instances'][0]['PublicIpAddress']


#execute a bash script to SSH to the EC2 hosts

os.chmod('deploy/connect.sh', 0o777)

if profile == 'sandbox':
    pass_arg=[]
    pass_arg.append("deploy/connect.sh")
    pass_arg.append("SBX-ed2-keypair.pem")
    pass_arg.append(EC2IP1)
    pass_arg.append(EC2IP2)
    pass_arg.append(RDSendpoint)
    subprocess.call(pass_arg)
if profile == 'sharedservices':
    subprocess.call(["deploy/connect.sh", "shs-ec2-keypair.pem", str(EC2IP1), str(RDSendpoint)])
    subprocess.call(["deploy/connect.sh", "shs-ec2-keypair.pem EC2IP2 RDSendpoint"])
if profile == 'nonprod':
    subprocess.call(["deploy/connect.sh", "npd-ec2-keypair.pem EC2IP1 RDSendpoint"])
    subprocess.call(["deploy/connect.sh", "npd-ec2-keypair.pem EC2IP2 RDSendpoint"])
if profile == 'production':
    subprocess.call(["deploy/connect.sh", "ppd-ec2-keypair.pem EC2IP1 RDSendpoint"])
    subprocess.call(["deploy/connect.sh", "ppd-ec2-keypair.pem EC2IP2 RDSendpoint"])
