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
    if os.path.isfile(archive_path) is False:
        return False
    try:
        # Get the archive filename without extension
        archive_name = os.path.basename(archive_path).split('.')[0]

        # Upload the archive to /tmp/ directory on the web servers
        put(archive_path, '/tmp/')

        # Create the release directory
        release_dir = '/data/web_static/releases/{}'.format(archive_name)
        run('sudo mkdir -p {}'.format(release_dir))

        # Uncompress the archive to the release directory
        run('sudo tar -xzf /tmp/{} -C {}'.format(
            os.path.basename(archive_path), release_dir
        ))

        # Remove the archive from the web server
        run('sudo rm /tmp/{}'.format(os.path.basename(archive_path)))

        # Move the files one directory up and delete the folder
        run('sudo mv {}/web_static/* {}'.format(release_dir, release_dir))
        run('sudo rm -rf {}/web_static'.format(release_dir))

        # Delete the current symbolic link
        current_link = '/data/web_static/current'
        run('sudo rm -rf {}'.format(current_link))

        # Create a new symbolic link
        run('sudo ln -s {} {}'.format(release_dir, current_link))

        # Restart the nginx service (if necessary)
        run('sudo service nginx restart')

        return True
    except Exception:
        return False
