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


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path_no_ext = "/data/web_static/releases/{}/".format(no_ext)
        symlink = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_no_ext))
        run("tar -xzf /tmp/{} -C {}".format(filename, path_no_ext))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(path_no_ext, path_no_ext))
        run("rm -rf {}web_static".format(path_no_ext))
        run("rm -rf {}".format(symlink))
        run("ln -s {} {}".format(path_no_ext, symlink))
        return True
    except Exception:
        return False
    