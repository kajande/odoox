import docker
import subprocess

from db import DB

class Odoox:
    
    client = docker.from_env()
    db = DB()

    def __init__(self, odoo_id=None, pg_id=None):
        ids = self.db.get()
        if ids:
            pg_id, odoo_id = ids
        self.pg_id = pg_id
        self.odoo_id = odoo_id

    def run(self, options):
        pg_options = {
            'image': 'postgres:15',
            'detach': True,
            'environment':{
                'POSTGRES_USER': 'odoo',
                'POSTGRES_PASSWORD': 'odoo',
                'POSTGRES_DB': 'postgres',
            },
            'name': 'pg',
        }

        odoo_options = {
            'image': 'odoo',
            'detach': True,
            'stdout': True,
            'stream': True,
            'ports': {
                '8069/tcp': 8069
            },
            'links': {
                'pg': 'db',
            },
            'tty': True,
            'name': 'odoo',
        }

        pg = self.client.containers.run(**pg_options)
        print(pg.id)
        odoo = self.client.containers.run(**odoo_options)
        print(odoo.id)
        
        self.db.save(pg.id, odoo.id)

        return odoo.logs(stream=True)


    def execute(self, command, options, pg=False, odoo=False):
        if '--pg' in options: options.remove('--pg')
        if '-g' in options: options.remove('-g')
        if '--odoo' in options: options.remove('--odoo')
        if '-o' in options: options.remove('-o')
        if pg:
            subprocess.run(['docker', command] + options + [self.pg_id])
        if odoo:
            subprocess.run(['docker', command] + options + [self.odoo_id])


if __name__ == '__main__':
    o = Odoox()
    o.execute('start')
