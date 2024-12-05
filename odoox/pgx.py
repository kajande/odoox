import psycopg2
from psycopg2 import sql
import configparser

from .config import config

class PG:
    def __init__(self):
        odoo_conf = configparser.ConfigParser()
        if config.get_docker_client():
            odoo_conf.read('./odoo.conf')
        else:
            odoo_conf.read('/etc/odoo/odoo.conf')

        pg_connect = config['pg_connect']
        self.host = pg_connect['host']
        self.port = pg_connect['port']
        self.dbname = odoo_conf['options']['db_name']
        self.user = pg_connect['user']
        self.password = pg_connect['password']

    def connect_and_execute(self, query):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()

            cursor.execute(query)
            if query.strip().lower().startswith("select"):
                results = cursor.fetchall()
                for row in results:
                    print(f"\n{row}\n")
            else:
                conn.commit()
            cursor.close()

            conn.close()

        except psycopg2.Error as e:
            print(f"An error occurred: {e}")

    def uninstall(self, module):
        query = f"""
        DELETE FROM ir_module_module where name='{module}' AND state='uninstalled';
        DELETE FROM ir_model_data WHERE module = 'base' AND name = 'module_{module}';
        """
        self.connect_and_execute(query)

pg = PG()

if __name__ == '__main__':
    query = "SELECT name, state FROM ir_module_module where name='demo' AND state='uninstalled';"
    pg.connect_and_execute(query)
