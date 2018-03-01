#!/bin/bash

ssh -i ~/.ssh/$1 ubuntu@$2 'git clone https://github.com/theITHollow/hollowapp.git'
#ssh -i ~/.ssh/$1 ubuntu@$2 "echo \"DATABASE_URL=mysql+pymysql://hollowapp:Password123@hollowappdb.awshollow.local:3306/hollowapp\" >> /home/ubuntu/hollowapp/.env"
ssh -i ~/.ssh/$1 ubuntu@$2 "ansible-playbook -i \"localhost,\" -c local /home/ubuntu/hollowapp/deploy/hollowappsetup.yml"

ssh -i ~/.ssh/$1 ubuntu@$3 'git clone https://github.com/theITHollow/hollowapp.git'
#ssh -i ~/.ssh/$1 ubuntu@$3 "echo \"DATABASE_URL=mysql+pymysql://hollowapp:Password123@hollowappdb.awshollow.local:3306/hollowapp\" >> /home/ubuntu/hollowapp/.env"
ssh -i ~/.ssh/$1 ubuntu@$3 "ansible-playbook -i \"localhost,\" -c local /home/ubuntu/hollowapp/deploy/hollowappsetup.yml"
