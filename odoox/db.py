import xmlrpc.client
import subprocess
import configparser

from .config import config

def execute(command, options):
    docker = config.get_docker_client()
    odoo_name = config.odoo_name
    db_name = command[0]
    if '-c' in options:
        options.remove('-c')
        if not docker:
            create_db(db_name, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} -c".split())
    elif '-s' in options:
        options.remove('-s')
        if not docker:
            select_db(db_name, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} -s".split())
            subprocess.run("odoox restart -o".split())
    elif '-d' in options:
        options.remove('-d')
        if not docker:
            delete_db(db_name, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} -d".split())
    elif '-l' in options:
        options.remove('-l')
        if not docker:
            list_db(db_name)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} -l".split())

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

def select_db(db_name, options):
    odoo_conf = configparser.ConfigParser()
    if config.get_docker_client():
        config_file = "./odoo.conf"
    else:
        config_file = "/etc/odoo/odoo.conf"
    try:
        odoo_conf.read(config_file)
        odoo_conf['options']['db_name'] = db_name

        # Write the changes back to the file
        with open(config_file, 'w') as file:
            odoo_conf.write(file)
        print(f"Database '{db_name}' selected successfully.")
    except Exception as e:
        print(e)


def list_db(owner):
    """
    List databases with the specified owner.
    :param owner: The owner is the current project name.
    """
    host = "localhost"
    port = 8069
    admin_password = "master"
    url = f"http://{host}:{port}/xmlrpc/2/db"
    db_proxy = xmlrpc.client.ServerProxy(url)

    try:
        # Fetch all databases
        databases = db_proxy.list(admin_password)

        # Placeholder for filtering (replace with actual filtering logic if available)
        filtered_dbs = [
            db for db in databases
            if db.startswith(owner)  # Assuming owner-based filtering logic
        ]

        import ipdb;ipdb.set_trace()

        for db in filtered_dbs:
            print(db)
        # return filtered_dbs
    except xmlrpc.client.Fault as e:
        print(f"Error occurred: {e.faultString}")
        return []
