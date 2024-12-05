import configparser

from .config import config

if config.get_docker_client():
    odoo_conf_file = './odoo.conf'
else:
    odoo_conf_file = '/etc/odoo/odoo.conf'

odoo_conf = configparser.ConfigParser()
odoo_conf.read(odoo_conf_file)
