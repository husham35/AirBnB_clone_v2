#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of `web_static`

# check and install nginx if not installed
if ! dpkg -l nginx >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# create all directories and sub-directories
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# create `index.html` in `test` directory
html_data="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"

echo "${html_data}" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# always create symbolic link even if it already exists
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# change owner and group for for the `/data/` directory
sudo chown -R ubuntu:ubuntu /data/

# configuration to add to `/etc/nginx/sites-available/default`
config_to_add="location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
        # Enable directory listing (if desired)
        # autoindex on;
    }"

nginx_config="/etc/nginx/sites-available/default"


# check if `/etc/nginx/sites-available/default` configuration already exists
if ! grep -q "location /hbnb_static/" "$nginx_config"; then
    # Configuration does not exist, add it using awk
    sudo awk -v config="$config_to_add" '/^}$/ {print config} {print} ' "$nginx_config" > temp && mv temp "$nginx_config"
    # sudo awk -v config="$config_to_add" '/^}$/ {print config} {print} ' "$nginx_config" | sudo tee "$nginx_config" > /dev/null

    echo "Configuration added."
else
    echo "Configuration already exists."
fi

sudo service nginx restart
