#!/bin/bash

sudo apt-get -y update
sudo apt-get -y install python3 python3-venv python3-dev elasticsearch supervisor nginx git

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn pymysql

echo "SECRET_KEY=52cb883e323b48d78a0a36e8e951ba4a" >> /home/ubuntu/hollowapp/.env
echo "MAIL_SERVER=localhost" >> /home/ubuntu/hollowapp/.env
echo "MAIL_PORT=25" >> /home/ubuntu/hollowapp/.env
echo "DATABASE_URL=mysql+pymysql://hollowapp:Password123@hollowappdb.cxnvq3t2hoei.us-east-1.rds.amazonaws.com/hollowapp" >> /home/ubuntu/hollowapp/.env
echo "ELASTICSEARCH_URI=http://localhost:9200" >> /home/ubuntu/hollowapp/.env

echo "export FLASK_APP=hollowapp.py">> ~/.profile
export FLASK_APP=hollowapp.py

flask db upgrade

sudo sed -i 's/#START_DAEMON=true/START_DAEMON=true'/g /etc/default/elasticsearch

sudo cp deploy/appSetup/hollowapp.conf /etc/supervisor/conf.d/hollowapp.conf

sudo supervisorctl reload

mkdir certs
openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout certs/key.pem -out certs/cert.pem -subj "/C=US/ST=Illinois/L=Chicago/O=theITHollow/CN=hollowapp.hollow.local"

sudo rm /etc/nginx/sites-enabled/default
sudo cp deploy/appSetup/hollowapp /etc/nginx/sites-enabled/hollowapp

sudo service nginx reload
