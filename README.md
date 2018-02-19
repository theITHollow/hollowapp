# Welcome to HollowApp!
#NOTE: for Jenkins to SSH into web server you must specify the private key such as : ssh -i ~/.ssh/SBX-ed2-keypair.pem ubuntu@IP.ADDRESS.GOES.HERE

This is a basic Flask Application used for demonstrating deployments.

To install the application
1. clone the repo
2. change directory to the repo root --> cd hollowapp
3. create an entrypoint --> export FLASK_APP=hollowapp.py
4. start virtual environment --> source venv/bin/activate
5. Run the flask application --> flask run



When making changes to the model database, be sure to run:
	Flask db migrate
And then
	Flask db upgrade

This schema changes into the flask sql database




This is an example application featured in my [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). See the tutorial for instructions on how to work with it.


To deploy the app on ubuntu with mysql, elasticsearch, gunicorn and nginx
##############

sudo apt-get -y update
sudo apt-get -y install python3 python3-venv python3-dev
sudo apt-get -y install mysql-server elasticsearch postfix supervisor nginx git

git clone https://github.com/theITHollow/hollowapp.git
cd hollowapp

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
pip install gunicorn pymysql

vi /home/ubuntu/hollowapp/.env

#Contents of file
SECRET_KEY=52cb883e323b48d78a0a36e8e951ba4a
MAIL_SERVER=localhost
MAIL_PORT=25
DATABASE_URL=mysql+pymysql://hollowapp:Password123@localhost:3306/hollowapp
ELASTICSEARCH_URI=http://localhost:9200


echo "export FLASK_APP=hollowapp.py" >> ~/.profile

mysql -u root -p

 create database hollowapp character set utf8 collate utf8_bin;
create user 'hollowapp'@'localhost' identified by 'Password123';
 grant all privileges on hollowapp.* to 'hollowapp'@'localhost';
flush privileges;
 quit;

flask db upgrade

#########
Comment out the line in /etc/default/elasticsearch
START_DAEMON=true

vi /etc/supervisor/conf.d/hollowapp.conf
#Contents of file
[program:hollowapp]
command=/home/ubuntu/hollowapp/venv/bin/gunicorn -b localhost:8000 -w 4 hollowapp:app
directory=/home/ubuntu/hollowapp
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true

sudo supervisorctl reload

mkdir certs
openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout certs/key.pem -out certs/cert.pem

sudo rm /etc/nginx/sites-enabled

vi /etc/nginx/sites-enabled/hollowapp
#contents

server {
	# listen on port 80 (http)
	listen 80;
	server_name _;
	location / {
		# redirect any requets to the same URL but on https
		return 301 https://$host$request_uri;
	}
}
server {
	# listen on port 443 (https)
	listen 443 ssl;
	server_name _;

	# location of the self-signed SSL certificate
	ssl_certificate /home/ubuntu/hollowapp/certs/cert.pem;
	ssl_certificate_key /home/ubuntu/hollowapp/certs/key.pem;

	# write access and error logs to /var/log
	access_log /var/log/hollowapp_access.log;
	error_log /var/log/hollowapp_error.log;

	location / {
		# forward application requests to the gunicorn server
		proxy_pass http://localhost:8000;
		proxy_redirect off;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}


}


sudo service nginx reload
