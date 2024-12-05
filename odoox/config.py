from pathlib import Path

class Config:
    def __init__(self):
        self.config = dict()
        project = {
            'path': '.', 
            'user': {
                'user': 'user', 
                'name': 'Moctar Diallo', 
                'email': 'moctarjallo@gmail.com'
            }
        }
        postgres = {
            'image': 'postgres:15', 
            'detach': True, 
            'environment': {
                'POSTGRES_USER': 'odoo', 
                'POSTGRES_PASSWORD': 'odoo', 
                'POSTGRES_DB': 'postgres'
            }
        }
        odoo = {
            'image': 'odoo', 
            'detach': True, 
            'stdout': True, 
            'stream': True, 
            'ports': {
                '8069/tcp': 8069
            }, 
            'tty': True
        }
        pg_connect = {
            'host': 'db', 
            'port': 5432, 
            'dbname': None, # from odoo_conf
            'user': 'odoo', 
            'password': 'odoo'
        }
        self.config['project'] = project
        self.config['postgres'] = postgres
        self.config['odoo'] = odoo
        self.config['pg_connect'] = pg_connect

    def __getitem__(self, item):
        return self.config[item]      

    def get_docker_client(self):
        try:
            import docker
            from docker.errors import DockerException
            client = docker.from_env()
            client.ping()
            return client
        except DockerException as e:
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")

    @property
    def project(self):
        return self.config['project']

    @property
    def user(self):
        return self.project['user']['user']

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

    @property
    def odoo_version(self):
        with open(self.project_path/'Dockerfile') as dockerfile:
            content = dockerfile.read()
            oi = content.find('odoo')
            version = content[oi:oi+len('odoo:xx')].split(':')[-1]
            return version

    @property
    def user_name(self):
        return self.project['user']['name']

    @property
    def user_email(self):
        return self.project['user']['email']
    
    def generate_postgres_options(self):
        options = self.config['postgres']
        cmd = []
        if options.get("detach", False):
            cmd.append("-d")
        environment = options.get("environment", {})
        for key, value in environment.items():
            cmd.append(f'-e "{key}={value}"')
        cmd.append(f'--name {self.pg_name}')
        image = options.get("image")
        if image:
            cmd.append(image)
        return " ".join(cmd)

        
config = Config()

if __name__ == '__main__':
    config = Config()
    command = config.generate_postgres_options()
    print(command)
    # print(config.odoo_version)
    # print(config.get_docker_client())
