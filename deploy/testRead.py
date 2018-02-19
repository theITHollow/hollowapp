import json


json_data=open('testread.json').read()

data = json.loads(json_data)
print(data)

print(data['EC2'])
print(data['RDS'])
