import yaml

PROJECT_PATH = './demo'

class Config:
    def __init__(self):
        self.config_path = PROJECT_PATH+'/config/odoox.yml'
        with open(self.config_path, 'r') as file:
            self.config = yaml.safe_load(file)        

    def __getitem__(self, key):
        return self.config[key]

if __name__ == '__main__':
    config = Config()
    print(config['odoo'])
