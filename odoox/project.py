from pathlib import Path
import subprocess

from .config import config

from .project_init import *


def execute(command, options):
    docker = config.get_docker_client()
    odoo_name = config.odoo_name
    odoo_version = config.odoo_version
    project_name = command[0]
    if '--init' in options:
        options.remove('--init')
        if not docker:
            init_project(project_name, odoo_version, options)
        else:
            subprocess.run(f"docker exec -it {odoo_name} odoox p {project_name} --init".split())


def init_project(name, odoo_version, options):
    project_dir = Path(name)
    project_dir.mkdir(exist_ok=True)

    get_dockerfile(project_dir, odoo_version)

    print(f"Project '{name}' created successfully.")
