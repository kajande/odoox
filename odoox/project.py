from pathlib import Path
import configparser

# from .config import config

from .gitx import *

def execute(command, options):
    # docker = config.get_docker_client()
    # odoo_version = config.odoo_version
    try:
        project_name = command[0]
    except IndexError:
        project_name = None
    if '--init' in options:
        init_project(project_name, options)

def init_project(project_name=None, options=None):
    # add ssh agent to prepare for github connection
    try:
        subprocess.run(["ssh-add", Path('~/.ssh/id_ed25519').expanduser()])
    except Exception:
        subprocess.run(["ssh-add", Path('~/.ssh/id_rsa').expanduser()])

    try:
        odoo_version = options[options.index('--init')+1]
    except IndexError:
        odoo_version = None
    repo_url = "https://github.com/kajande/odoox_project_template.git"
    clone_and_checkout(repo_url, target_dir=project_name, branch=odoo_version)
    project_dir = Path(f'./{project_name}') if project_name else Path('.')
    project_name = project_dir.resolve().stem
    update_db_name(project_dir/'odoo.conf', project_name)

    print(f"Project '{project_name}' created successfully.")

def update_db_name(file_path, db_name):
    config = configparser.ConfigParser()
    config.read(file_path)

    config['options']['db_name'] = db_name

    with open(file_path, 'w') as configfile:
        config.write(configfile)
