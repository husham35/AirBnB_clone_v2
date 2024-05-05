#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy:
 - Prototype: def do_deploy(archive_path):
 - Returns False if the file at the path archive_path doesn’t exist
 - The script should take the following steps:
 -  - Upload the archive to the /tmp/ directory of the web server
 -  - Uncompress the archive to the folder /data/web_static/releases/<archive
      filename without extension> on the web server
 -  - Delete the archive from the web server
 -  - Delete the symbolic link /data/web_static/current from the web server
 -  - Create a new the symbolic link /data/web_static/current
      on the web server, linked to the new version of your code 
	  (/data/web_static/releases/<archive filename without extension>)
 - All remote commands must be executed on your both web servers
   (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
 - Returns True if all operations have been done correctly,
   otherwise returns False
 - You must use this script to deploy it on your servers:
   xx-web-01 and xx-web-02
"""
from fabric.api import env, put, run
import os.path

env.hosts = ['54.83.170.40', '18.209.179.183']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1].split(".")[0]

        put(archive_path, '/tmp/')
        run('mkdir /data/web_static/releases/{}'.format(file_name))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}'.
            format(file_name, file_name))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.
            format(file_name, file_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(file_name))
        run('rm -rf /tmp/{}.tgz'.format(file_name))
        run('rm -rf /data/web_static/current')
        run('ln -sf /data/web_static/releases/{}/ /data/web_static/current'.
            format(file_name))
        return True
    except Exception:
        return False
    