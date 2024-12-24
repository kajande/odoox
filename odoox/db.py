import psycopg2
from psycopg2 import sql
import xmlrpc.client
import odoorpc
import subprocess
import configparser

from .config import config

def execute(command, options):
    docker = config.get_docker_client()
    odoo_name = config.odoo_name
    try:
        db_name = command[0]
    except IndexError as ie:
        db_name = config.current_db
    if '-s' in options:
        options.remove('-s')
        if not docker:
            select_db(db_name, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} -s".split())
            subprocess.run("odoox restart -o".split())
    elif '-c' in options:
        options.remove('-c')
        if not docker:
            create_db(db_name, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} -c".split())
    elif '-d' in options:
        options.remove('-d')
        if not docker:
            delete_db(db_name, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} -d".split())
    elif '-l' in options:
        options.remove('-l')
        # if not docker:
        list_db(db_name)
        # else:
        #     subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} -l".split())

    elif '--debug' in options:
        options.remove('--debug')
        if not docker:
            debug_db(db_name, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox db {db_name} --debug".split())
    if options:
        if '-c' in options or '-s' in options or '-d' in options:
            subprocess.run(["odoox", "db"] + [db_name] + options)
        subprocess.run(["odoox"] + command[1:] + options)

def create_db(db_name, options):
    db_name = config.project_name + "_" + db_name
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
    db_name = config.project_name + "_" + db_name
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
    db_name = config.project_name + "_" + db_name
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


def list_db(db_name):
    """
    List databases with the specified owner.
    :param db_name: The name of the database to list.
    """

    host = "localhost"
    port = 5432
    user = "odoo"
    password = "odoo"
    owner = config.project_name

    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Query to list databases owned by the specified owner
        query = sql.SQL("SELECT datname FROM pg_database WHERE datdba = (SELECT usesysid FROM pg_user WHERE usename = %s)")
        cursor.execute(query, (owner,))
        db_list = cursor.fetchall()

        print("Databases:")
        for db in db_list:
            db = db[0]
            if db == config.current_db:
                print(f"* {db}")
            else:
                print(db)

        cursor.close()
        conn.close()
        return [db[0] for db in db_list]

    except psycopg2.Error as e:
        print(f"Error: {e}")
        return []


def debug_db(db, options):
    host = "localhost"
    port = 8069
    user = "admin"
    password = "admin"
    try:
        odoo = odoorpc.ODOO(host, port=port)
        odoo.login(db, user, password)

        Module = odoo.env['ir.module.module']

        import ipdb;ipdb.set_trace()

    except odoorpc.error.RPCError as e:
        print(f"An error occurred while upgrading the module: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
