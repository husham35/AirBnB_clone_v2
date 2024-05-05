#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy:
Prototype: def deploy():
 - The script should take the following steps:
 - Call the do_pack() function and store the path of the created archive
 - Return False if no archive has been created
 - Call the do_deploy(archive_path) function, using the new path
   of the new archive
 - Return the return value of do_deploy
 - All remote commands must be executed on both of web your servers
   (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
 - You must use this script to deploy it on your servers:
   xx-web-01 and xx-web-02
"""
from fabric.api import env, put, run, local
import os.path
from time import strftime

env.hosts = ['54.83.170.40', '18.209.179.183']
env.user = 'ubuntu'


def do_pack():
    """create a .tgz archive of the `web_static/` directory"""
    timenow = strftime("%Y%M%d%H%M%S")
    try:
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(timenow)
        local("tar -cvzf {} web_static/".format(filename))
        return filename
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        # Get the archive filename without extension
        archive_name = os.path.basename(archive_path).split('.')[0]

        # Upload the archive to `/tmp/` directory on the web servers
        put(archive_path, '/tmp/')

        # Create the `release` directory
        release_dir = '/data/web_static/releases/{}'.format(archive_name)
        run('sudo mkdir -p {}'.format(release_dir))

        # Decompress the archive to the release directory
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

        # Restart the nginx service
        run('sudo service nginx restart')

        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to your web servers"""
    result = do_pack()
    final_deploy = do_deploy(result) if result else False
    return final_deploy


def do_clean(number=0):
    """ Deletes old versions of deployed tgz files """

    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
