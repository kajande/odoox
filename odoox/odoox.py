import subprocess
import xmlrpc.client

import configparser
from pathlib import Path
import shutil

from .config import config
from .pgx import pg
from . import gitx

def execute(command, options):
    if command[0] == 'm':
        if '-i' in options:
            module = options[options.index('-i')+1]
            install_module(module, options)
        if '--i' in options:
            module = options[options.index('--i')+1]
            uninstall_module(module, options) 
        if '-l' in options:
            list(options)
    if command[0] == 'db':
        db_name = command[1]
        if '-c' in options:
            if not config.get_docker_client():
                create_db(db_name, options)
                options.remove('-c')
            else:
                subprocess.run(f"docker exec -it demo_odoo odoox db {db_name} -c".split())

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

def create_db(db_name, options):

    host = "localhost"  # Odoo server host
    port = 8069         # Odoo server port
    super_admin_password = "master"  # Master password for database management
    demo_data = False                # Use demo data? (True/False)
    lang = "en_US"                   # Default language for the database

    # Construct the full URL for the XML-RPC endpoint
    url = f"http://{host}:{port}/xmlrpc/2/db"

    # Create the XML-RPC client proxy for the 'db' service
    db_proxy = xmlrpc.client.ServerProxy(url)

    try:
        # Use the `create_database` method for database creation
        db_proxy.create_database(
            super_admin_password,  # Master password
            db_name,               # Database name
            demo_data,             # Demo data
            lang                   # Language
        )
        print(f"Database '{db_name}' created successfully.")
    except xmlrpc.client.Fault as e:
        print(f"Error occurred: {e.faultString}")
