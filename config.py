from pathlib import Path
import yaml

PROJECT_PATH = './demo'

class Config:
    def __init__(self):
        self.config_path = PROJECT_PATH+'/config/odoox.yml'
        with open(self.config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def __getitem__(self, item):
        return self.config[item]      

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

if __name__ == '__main__':
    config = Config()
    import ipdb;ipdb.set_trace()
    print(config['odoo'])
