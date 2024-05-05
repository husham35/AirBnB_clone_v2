#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of `web_static`

ADD_WEBSTATIC="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/
sudo sed -i "35i $ADD_WEBSTATIC" /etc/nginx/sites-available/default
sudo service nginx start
