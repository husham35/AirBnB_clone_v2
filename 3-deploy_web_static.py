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
import os
import datetime
import tarfile

env.hosts = ['54.83.170.40', '18.209.179.183']
env.user = 'ubuntu'


def do_pack():
    """create a .tgz archive of the `web_static/` directory"""
    try:
        # get the current working directory (where the script is located)
        current_directory = os.getcwd()

        # define the name of the archive
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = 'web_static_{}.tgz'.format(timestamp)

        # define the path to the version folder
        versions_folder = os.path.join(current_directory, 'versions')

        # create the versions folder if it doesn't exist
        if not os.path.exists(versions_folder):
            os.makedirs(versions_folder)

        # function to filter out hidden directories and files
        def is_hidden(path):
            return os.path.basename(path).startswith('.')

        # create the full path to the archive
        archive_path = os.path.join(versions_folder, archive_name)

        # create a .tgz archive, excluding hidden directories/files
        with tarfile.open(archive_path, 'w:gz') as tar:
            for root, dirs, files in os.walk(current_directory):
                # exclude hidden directories
                dirs[:] = [
                    d for d in dirs if not is_hidden(os.path.join(root, d))
                ]
                for file in files:
                    # exclude hidden files
                    if not is_hidden(file):
                        file_path = os.path.join(root, file)
                        tar.add(
                            file_path, arcname=os.path.relpath(
                                file_path, current_directory)
                        )

        return archive_path

    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # get the archive filename without extension
        archive_name = os.path.basename(archive_path).split('.')[0]

        # upload the archive to /tmp/ directory on the web servers
        put(archive_path, '/tmp/')

        # create the release directory
        release_dir = '/data/web_static/releases/{}'.format(archive_name)
        run('mkdir -p {}'.format(release_dir))

        # decompress the archive to the release directory
        run('tar -xzf /tmp/{} -C {}'.format(
            os.path.basename(archive_path), release_dir
        ))

        # remove the archive from the web server
        run('rm /tmp/{}'.format(os.path.basename(archive_path)))

        # move the files one directory up and delete the folder
        run('mv {}/web_static/* {}'.format(release_dir, release_dir))
        run('rm -rf {}/web_static'.format(release_dir))

        # delete and create the current symbolic link
        current_link = '/data/web_static/current'
        run('rm -rf {}'.format(current_link))
        run('ln -s {} {}'.format(release_dir, current_link))

        # restart the nginx service
        run('sudo service nginx restart')

        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    return False if archive_path is None else do_deploy(archive_path)
