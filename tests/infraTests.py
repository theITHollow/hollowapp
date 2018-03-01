#!/usr/bin/python
import boto3
import time
import json
import sys, os

session = boto3.Session(profile_name='sandbox')
client = session.client('cloudformation')

#functions
def status(stack):
    stackStatus = client.describe_stacks(StackName=stack)
    status=(stackStatus['Stacks'][0]['StackStatus'])
    print "{}'s current status is {}.".format(stack, status)
    if (status != 'CREATE_COMPLETE'):
        sys.exit(-1)



status('HollowApp-RDS')

status('HollowApp-EC2-LB')
