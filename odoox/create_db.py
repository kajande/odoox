import xmlrpc.client
import sys

def create_odoo_database():
    # Odoo server details
    url = 'http://localhost:1769'
    db = 'postgres'  # The default database (used for system operations)
    username = 'admin'
    password = 'admin'

    # Authentication to get the user ID
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})

    # Create a new database (requires the master password)
    object = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/db')
    master_password = 'admin'

    new_db = 'new_database_name'  # Customize this as needed

    try:
        # Create the new database
        object.create_database(db, new_db, master_password, False, 'en_US', 'admin', 'admin')
        print(f"Database '{new_db}' created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_odoo_database()
