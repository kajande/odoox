from pathlib import Path
import configparser
import os
import socket
import docker
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

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
        self.config['project'] = project
        postgres = {
            'image': 'postgres:15', 
            'detach': True, 
            'environment': {
                'POSTGRES_USER': 'odoo', 
                'POSTGRES_PASSWORD': 'odoo', 
                'POSTGRES_DB': 'postgres'
            }
        }
        self.config['postgres'] = postgres
        odoo = {
            'image': 'odoo', 
            'detach': False,
            'stdout': True, 
            'stream': True, 
            'ports': {
                '8069/tcp': 8069
            }, 
            'tty': True
        }
        odoo['volumes'] = {
            str(self.project_path): {
                'bind': f"/{self.project_name}",
                'mode': 'rw',
            },
            str(self.project_path/"odoo.conf"): {
                'bind': "/etc/odoo/odoo.conf",
                'mode': 'rw',
            },
        }
        odoo['name'] = self.odoo_name
        odoo['links'] = {
            self.pg_name: 'db'
        }
        self.config['odoo'] = odoo
        pg_connect = {
            'host': 'db', 
            'port': 5432, 
            'dbname': None, # from odoo_conf
            'user': 'odoo', 
            'password': 'odoo'
        }
        self.config['pg_connect'] = pg_connect

        self.odoo_conf = configparser.ConfigParser()
        if self.get_docker_client():
            odoo_conf_file = './odoo.conf'
        else:
            odoo_conf_file = '/etc/odoo/odoo.conf'
        self.odoo_conf.read(odoo_conf_file)

    @property
    def base_data_path(self):
        path = Path.home()/ '.odoox' / self.project_name
        path.mkdir(parents=True, exist_ok=True)
        return path

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
    
    @property
    def git_token(self):
        return os.environ['GIT_TOKEN']

    @property
    def current_db(self):
        return self.odoo_conf['options']['db_name']
    
    @property
    def odoo_ip(self):
        if self.get_docker_client():
            try:
                client = docker.from_env()  # Initialize the Docker client
                container = client.containers.get(self.odoo_name)  # Get the container by name
                network_settings = container.attrs['NetworkSettings']['Networks']  # Access network settings
                # Retrieve the IP address from the first network
                ip_address = next(iter(network_settings.values()))['IPAddress']
                return ip_address
            except docker.errors.NotFound:
                return f"Error: Container '{self.odoo_name}' not found."
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            try:
                hostname = socket.gethostname()
                return socket.gethostbyname(hostname)
            except socket.error as e:
                return f"Error: {e}"


    def generate_postgres_options(self, options):
        pg_options = self.config['postgres']
        cmd = []
        if pg_options.get("detach", False):
            cmd.append("-d")
        environment = pg_options.get("environment", {})
        for key, value in environment.items():
            cmd.append(f'-e {key}={value}')
        cmd.append(f'--name {self.pg_name}')
        image = pg_options.get("image")
        if image:
            cmd.append(image)
        return " ".join(cmd)

    def generate_odoo_options(self, tag, port, options=None):
        odoo_options = self.config['odoo']
        cmd = []

        # Handle detach mode
        if odoo_options.get("detach", False) or '-d' in options:
            cmd.append("-d")

        # Handle ports
        # set port for current image (--dev mode)
        odoo_options['ports']['8069/tcp'] = f"{port}69"
        ports = odoo_options.get("ports", {})
        for container_port, host_port in ports.items():
            cmd.append(f'-p {host_port}:{container_port.split("/")[0]}')

        volumes = odoo_options.get("volumes", {})
        for host_path, volume_details in volumes.items():
            bind = volume_details.get("bind")
            cmd.append(f'-v {host_path}:{bind}')
        # mount ssh agent forwarding
        os.environ["SSH_AUTH_SOCK"]
        cmd.append(f' -v {os.environ["SSH_AUTH_SOCK"]}:/ssh-agent')
        cmd.append(' -e SSH_AUTH_SOCK=/ssh-agent')

        links = odoo_options.get("links", {})
        for container_name, alias in links.items():
            cmd.append(f'--link {container_name}:{alias}')

        if odoo_options.get("tty", False):
            cmd.append("--tty")

        container_name = odoo_options.get("name")
        if container_name:
            cmd.append(f'--name {container_name}')

        odoo_options['image'] = tag
        image = odoo_options.get("image", "latest")
        cmd.append(image)

        return " ".join(cmd)


config = Config()

if __name__ == '__main__':
    config = Config()
    # command = config.generate_postgres_options([])
    # print(command)
    tag = "latest"
    port = 17

    odoo_options = config['odoo']
    command = config.generate_odoo_options(tag, port, config['odoo'])
    print(command)
    import ipdb;ipdb.set_trace()
    # print(config.odoo_version)
    # print(config.get_docker_client())
