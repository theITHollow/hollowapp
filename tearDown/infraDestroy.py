#!/usr/bin/python
import boto3
import time
import json
import sys, os

session = boto3.Session(profile_name='sandbox')
client = session.client('cloudformation')

#functions
def delete(stack):
    stackStatus = client.describe_stacks(StackName=stack)
    status=(stackStatus['Stacks'][0]['StackStatus'])
    print "{}'s current status is {}.".format(stack, status)
    if (status == 'CREATE_COMPLETE'):
        response = client.delete_stack(StackName=stack)
        print "Stack is being deleted"


delete('HollowApp-RDS')
print "HollowApp-RDS is now being deleted"

delete('HollowApp-EC2-LB')
print "HollowApp-EC2-LB is now being deleted"
