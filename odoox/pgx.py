import psycopg2
from psycopg2 import sql

class PG:
    def __init__(self):
        self.host = 'db'
        self.port = 5432
        self.dbname = 'test17'
        self.user = 'odoo'
        self.password = 'odoo'

    def execute(self, cursor, query):
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
            for row in results:
                print(f"\n{row}\n")
        else:
            conn.commit()
        cursor.close()

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

            self.execute(cursor, query)

            conn.close()

        except psycopg2.Error as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    pg = PG()
    query = "SELECT name, state FROM ir_module_module where name='demo';"

    pg.connect_and_execute(query)
