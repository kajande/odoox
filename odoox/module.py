from pathlib import Path
import shutil
import configparser
import subprocess

import odoorpc

from .config import config
from .odoo_conf import odoo_conf
from .pgx import pg
from . import gitx

def execute(command, options):
    docker = config.get_docker_client()
    odoo_name = config.odoo_name
    db_name = odoo_conf['options']['db_name']
    module = command[0]
    if '-i' in options:
        options.remove('-i')
        if not docker:
            install_module(module, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox m {module} -i".split())
    if '--i' in options:
        options.remove('--i')
        if not docker:
            uninstall_module(module, options) 
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox m {module} --i".split())
    if '-l' in options:
        options.remove('-l')
        if not docker:
            list(options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox m {module} -l".split())
    
    if '-a' in options:
        options.remove('-a')
        if not docker:
            activate_module(module, db_name, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox m {module} -a".split())

    if '--a' in options:
        options.remove('--a')
        if not docker:
            deactivate_module(module, db_name, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox m {module} --a".split())

    if options:
            subprocess.run(f"odoox {' '.join(options)}".split())

def uninstall_dependency(dep_module, dest_dir):
    """
    Removes a module from the destination directory if it exists.
    """
    module_path = dest_dir / dep_module
    if module_path.exists() and module_path.is_dir():
        try:
            shutil.rmtree(module_path)
            pg.uninstall(dep_module)
            print(f"Uninstalled '{dep_module}'")
        except Exception as e:
            print(f"Error removing extra module '{dep_module}': {e}")


def install_module(module, options):
    """
    Copies specified modules from the source directory to the destination directory,
    and removes any extra modules not listed in the configuration file.
    """
    module_path = Path(f"./{module}")
    BASE_DEPS_DIR = Path("xaddons")
    DEST_DIR = Path("/mnt/extra-addons")

    config = configparser.ConfigParser()
    config.read(f"{module}/gitx.conf")

    dep_modules = set(config.sections())

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    # Find and remove extra modules
    existing_modules = {p.name for p in DEST_DIR.iterdir() if p.is_dir()}
    for extra_module in existing_modules - dep_modules - {module}:
        uninstall_dependency(extra_module, DEST_DIR)

    # Copy modules listed in the config file
    for dep_module in dep_modules:
        pull_uri = config[dep_module].get('pulluri', '')
        if not pull_uri:
            print(f"Warning: No pull URI defined for module '{dep_module}'")
            continue

        try:
            org, repo = pull_uri.split('/')[-2:]
            repo = repo.replace('.git', '')
            source_path = BASE_DEPS_DIR.joinpath(org, repo, dep_module)
            dest_path = DEST_DIR / dep_module

            if not source_path.exists():
                clone_args = {
                    "repo_url": pull_uri,
                    "branch": config[dep_module].get('track', 'main'),
                    "commit_hash": config[dep_module].get('track', ''),
                    "target_dir": BASE_DEPS_DIR/org/repo,
                }
                gitx.clone_and_checkout(**clone_args)

            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
            print(f"Installed '{dep_module}'")
        except Exception as e:
            print(f"Error processing module '{dep_module}': {e}")
    # Finally install the parent module
    shutil.copytree(module_path, DEST_DIR/module_path, dirs_exist_ok=True)
    print(f"Installed '{module}'")
    update_apps_list(odoo_conf['options']['db_name'])

def uninstall_module(module, options):
    """
    Uninstalls the specified module and its dependencies.
    """
    DEST_DIR = Path("/mnt/extra-addons")

    module_path = Path(f"./{module}")
    BASE_DEPS_DIR = Path("xaddons")

    config = configparser.ConfigParser()
    config.read(f"{module}/gitx.conf")

    dep_modules = set(config.sections())

    # Uninstall dependencies recursively
    for dep_module in dep_modules:
        uninstall_dependency(dep_module, DEST_DIR)

    # Now uninstall the main module
    uninstall_dependency(module, DEST_DIR)

    # Remove from postgres db
    pg.uninstall(module)

def list(options):
    subprocess.run("ls /mnt/extra-addons".split())



def update_apps_list(db_name):
    """
    Update the Odoo apps list.

    :param host: Host where Odoo is running (e.g., "localhost").
    :param port: Port where Odoo is running (e.g., 8069).
    :param database: Name of the database to connect to.
    :param username: Username for Odoo authentication.
    :param password: Password for Odoo authentication.
    """
    host = "localhost"
    port = 8069
    database = db_name
    username = "admin"
    password = "admin"
    try:
        odoo = odoorpc.ODOO(host, port=port)
        odoo.login(database, username, password)
        module_model = odoo.env['ir.module.module']
        module_model.update_list()
        print("Apps list updated.")
    except Exception as e:
        print(f"Error occurred: {e}")

def activate_module(module, db, options):
    host = "localhost"
    port = 8069
    admin_user = "admin"
    admin_password = "admin"
    try:
        odoo = odoorpc.ODOO(host, port=port)        
        odoo.login(db, admin_user, admin_password)        
        module_model = odoo.env['ir.module.module']
        module_ids = module_model.search([('name', '=', module)])
        
        if not module_ids:
            subprocess.run(f"odoox m -i {module}".split())
            module_ids = module_model.search([('name', '=', module)])
        
        module_record = module_model.browse(module_ids[0])
        if module_record.state != 'installed':
            print(f"Installing module '{module}'...")
            module_model.button_immediate_install([module_record.id])
            print(f"Module '{module}' installed successfully.")
        else:
            print(f"Module '{module}' is already installed.")
    
    except odoorpc.error.RPCError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def deactivate_module(module, db, options):
    host = "localhost"
    port = 8069
    admin_user = "admin"
    admin_password = "admin"
    try:
        odoo = odoorpc.ODOO(host, port=port)        
        odoo.login(db, admin_user, admin_password)        
        module_model = odoo.env['ir.module.module']        
        module_ids = module_model.search([('name', '=', module)])
        
        if not module_ids:
            print(f"Module '{module}' not found.")
            return
        
        module_record = module_model.browse(module_ids[0])
        if module_record.state == 'installed':
            print(f"Uninstalling module '{module}'...")
            module_model.button_immediate_uninstall([module_record.id])
            print(f"Module '{module}' uninstalled successfully.")
        else:
            print(f"Module '{module}' is not installed or is already uninstalled.")
    
    except odoorpc.error.RPCError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
