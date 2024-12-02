from pathlib import Path
import yaml


class Config:
    def __init__(self):
        self.config_path = './odoox.yml'
        with open(self.config_path, 'r') as file:
            self.config = yaml.safe_load(file)

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
        
config = Config()

if __name__ == '__main__':
    config = Config()
    print(config.odoo_version)
    print(config.get_docker_client())
