from .dockerx import Dockerx
import subprocess

from . import module
from . import db
from . import project

def execute(command, options):
    if command[0] == 'm':
        module.execute(command[1:], options)
    if command[0] == 'db':
        db.execute(command[1:], options)
    if command[0] == 'p':
        project.execute(command[1:], options)
    if command[0] == 'k':
        try:
            subprocess.run(f"odooxia k {command[1]}".split() + options)
        except Exception:
            print("You probably don't have access to `odooxia` !")
