import xmlrpc.client
import subprocess

from .config import config

def execute(command, options):
    docker = config.get_docker_client()
    odoo_name = config.odoo_name
    db_name = command[0]
    if '-c' in options:
        if not docker:
            create_db(db_name, options)
            options.remove('-c')
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} -c".split())
    if '-d' in options:
        if not docker:
            delete_db(db_name, options)
            options.remove('-d')
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} -d".split())

def create_db(db_name, options):
    host = "localhost"
    port = 8069
    super_admin_password = "master"
    demo_data = False
    lang = "en_US"

    url = f"http://{host}:{port}/xmlrpc/2/db"

    db_proxy = xmlrpc.client.ServerProxy(url)

    try:
        db_proxy.create_database(
            super_admin_password,
            db_name,
            demo_data,
            lang
        )
        print(f"Database '{db_name}' created successfully.")
    except xmlrpc.client.Fault as e:
        print(f"Error occurred: {e.faultString}")


def delete_db(db_name, options):
    host = "localhost"
    port = 8069
    super_admin_password = "master"

    url = f"http://{host}:{port}/xmlrpc/2/db"
    db_proxy = xmlrpc.client.ServerProxy(url)

    try:
        db_proxy.drop(super_admin_password, db_name)
        print(f"Database '{db_name}' deleted successfully.")
    except xmlrpc.client.Fault as e:
        print(f"Error occurred: {e.faultString}")
