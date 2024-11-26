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
    def user(self):
        return self.project['user']

    @property
    def repo(self):
        return f"{self.user}/{self.project_name}"

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
            tag = self.project['user'] + '/' + path.stem + ':' + options.pop(t_index+1)
            options.insert(t_index+1, tag)
        else:
            tag = self.project['user'] + '/' + path.stem + ':latest'
            options.append('-t')
            options.append(tag)
        options.append(str(path))
        subprocess.run(['docker', 'buildx', 'build'] + options)
        return tag


    def run(self, options):
        if '-b' in options:
            options.remove('-b')
            tag = self.build(options)
        elif '-t' in options:
            t = options.pop(options.index('-t')+1)
            tag = self.project['user'] + '/' + self.project_path.stem + f':{t}'
        else:
            t = 'latest'
            tag = self.project['user'] + '/' + self.project_path.stem + f':{t}'

        pg_options = self.config['postgres']
        odoo_options = self.config['odoo']
        odoo_options['image'] = tag
        
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
        if '-og' in options: options.remove('-og')
        if '-go' in options: options.remove('-go')
        if command == 'start':
            self.start_container(pg, odoo, options)
            return
        if command == 'rm':
            options = ['-vf'] + options
        if pg:
            subprocess.run(['docker', command] + options + [self.pg_name])
        if odoo:
            subprocess.run(['docker', command] + options + [self.odoo_name])
        if command == 'ps':
            self.list_containers(options)
        if command == 'image':
            if '--rm' in options:
                self.remove_image(options)
        if command == 'images':
            self.list_images(options)

    def start_container(self, pg, odoo, options):
        if pg:
            pg_exists = self.client.containers.list(all=True, filters={
                'name': f"{self.project_name}_pg"
            })
            if pg_exists:
                subprocess.run(['docker', 'start'] + [pg_exists[0].id] + options)
            else:
                pg_options = self.config['postgres']
                pg_options['name'] = self.pg_name
                pg = self.client.containers.run(**pg_options)
                print(f"{self.pg_name}: {pg.id}")

        if odoo:
            odoo_exists = self.client.containers.list(all=True, filters={
                'name': f"{self.project_name}_odoo"
            })
            if odoo_exists:
                subprocess.run(['docker', 'start'] + [odoo_exists[0].id] + options)
            else:
                odoo_options = self.config['odoo']
                odoo_options['image'] = f"{self.repo}:latest"
                odoo_options['name'] = self.odoo_name
                odoo_options['links'] = {
                    self.pg_name: 'db'
                }
                odoo_container = self.client.containers.run(**odoo_options)
                print(f"{self.odoo_name}: {odoo_container.id}")


    def list_containers(self, options):
        subprocess.run(['docker', 'ps', '-f', f"name={self.project_name}*"] + options)

    def list_images(self, options):
        subprocess.run(['docker', 'images'] + [f"{self.user}/{self.project_name}"] + options)

    def remove_image(self, options):
        tag = options[options.index('--rm')+1]
        options.remove('--rm')
        options.remove(tag)
        command = ['docker', 'image', 'rm', '-f'] + [f"{self.user}/{self.project_name}:{tag}"] + options
        subprocess.run(command)

if __name__ == '__main__':
    o = Odoox()
    o.execute('start')
