import subprocess
import xmlrpc.client

import configparser
from pathlib import Path
import shutil

from .config import config
from . import gitx
from . import module

def execute(command, options):
    if command[0] == 'm':
        module.execute(command[1:], options)
    if command[0] == 'db':
        db_name = command[1]
        if '-c' in options:
            if not config.get_docker_client():
                create_db(db_name, options)
                options.remove('-c')
            else:
                subprocess.run(f"docker exec -it demo_odoo odoox db {db_name} -c".split())


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
