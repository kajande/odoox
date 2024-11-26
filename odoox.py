import docker
import subprocess
from pathlib import Path

from config import Config

class Odoox:
    
    client = docker.from_env()
    config = Config()

    @property
    def project(self):
        return self.config['project']

    @property
    def project_path(self):
        return Path(self.project['path']).resolve()

    @property
    def project_name(self):   
        return self.project_path.stem
    
    @property
    def pg_name(self):
        return self.project_name + '_pg'
    
    @property
    def odoo_name(self):
        return self.project_name + '_odoo'
    
    def build(self, options):
        path = self.project_path
        if '-t' in options:
            t_index = options.index('-t')
            tag = self.project['user'] + '/' + path.stem + ':' + options[t_index+1]
            options[t_index+1] = tag
        else:
            tag = self.project['user'] + '/' + path.stem + ':latest'
            options.append('-t')
            options.append(tag)
        options.append(str(path))
        subprocess.run(['docker', 'buildx', 'build'] + options)


    def run(self, options):
        self.build(options)
        pg_options = self.config['postgres']
        odoo_options = self.config['odoo']
        odoo_options['image'] = options[options.index('-t')+1]
        
        pg_options['name'] = self.pg_name
        odoo_options['name'] = self.odoo_name
        odoo_options['links'] = {
            self.pg_name: 'db'
        }

        pg = self.client.containers.run(**pg_options)
        print(f"{self.pg_name}: {pg.id}")
        odoo = self.client.containers.run(**odoo_options)
        print(f"{self.odoo_name}: {odoo.id}")

        if not odoo_options['detach']:
            for log in odoo:
                print(log.get("stream", "").strip())


    def execute(self, command, options, pg=False, odoo=False):
        if '--pg' in options: options.remove('--pg')
        if '-g' in options: options.remove('-g')
        if '--odoo' in options: options.remove('--odoo')
        if '-o' in options: options.remove('-o')
        if pg:
            subprocess.run(['docker', command] + options + [self.pg_name])
        if odoo:
            subprocess.run(['docker', command] + options + [self.odoo_name])
        if command == 'ps':
            self.list_containers(options)

    def list_containers(self, options):
        subprocess.run(['docker', 'ps', '-f', f"name={self.project_name}*"] + options)


if __name__ == '__main__':
    o = Odoox()
    o.execute('start')
