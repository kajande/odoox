from .dockerx import Dockerx

from . import module
from . import db

def execute(command, options):
    if command[0] == 'm':
        module.execute(command[1:], options)
    if command[0] == 'db':
        db.execute(command[1:], options)