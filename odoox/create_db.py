import xmlrpc.client
import sys
import odoorpc

def create_odoo_database():

    # Configuration
    host = "localhost"  # Odoo server host
    port = 8069         # Odoo server port
    super_admin_password = "master"  # Master password for database management
    db_name = "test17bis"               # Name of the new database
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




    #####################WORKS###############################
    # # Connect to the Odoo instance
    # odoo = odoorpc.ODOO('localhost', port=8069)

    # # Authenticate as the admin user
    # odoo.login('test17', 'moctar.diallo@kajande.com')

    # import ipdb;ipdb.set_trace()

    # # Create a new database
    # db_name = 'my_new_db'
    # odoo.db.create('master', db_name, demo=False, lang='en_US')
    #####################WORKS###############################


if __name__ == "__main__":
    create_odoo_database()
