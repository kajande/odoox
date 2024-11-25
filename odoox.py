import docker
import subprocess
from pathlib import Path

from config import Config

class Odoox:
    
    client = docker.from_env()
    config = Config()

    @property
    def project_name(self):   
        return Path(self.config['project']['path']).resolve().stem
    
    @property
    def pg_name(self):
        return self.project_name + '_pg'
    
    @property
    def odoo_name(self):
        return self.project_name + '_odoo'

    def run(self, options):
        pg_options = self.config['postgres']
        odoo_options = self.config['odoo']

        pg_options['name'] = self.pg_name
        odoo_options['name'] = self.odoo_name
        odoo_options['links'] = {
            self.pg_name: 'db'
        }

        pg = self.client.containers.run(**pg_options)
        print(pg.id)
        odoo = self.client.containers.run(**odoo_options)
        print(odoo.id)

        return odoo.logs(stream=True)


    def execute(self, command, options, pg=False, odoo=False):
        if '--pg' in options: options.remove('--pg')
        if '-g' in options: options.remove('-g')
        if '--odoo' in options: options.remove('--odoo')
        if '-o' in options: options.remove('-o')
        if pg:
            subprocess.run(['docker', command] + options + [self.pg_name])
        if odoo:
            subprocess.run(['docker', command] + options + [self.odoo_name])


if __name__ == '__main__':
    o = Odoox()
    o.execute('start')
