import argparse
import subprocess

from odoox import Dockerx
from odoox import odoox

from .config import config

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', nargs="*")
    parser.add_argument('options', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if config.get_docker_client():
        dockerx = Dockerx()

        if args.command[0] == 'docker':
            subprocess.run(args.command + args.options)
        elif args.command[0] == 'build':
            dockerx.build(args.options)
        elif args.command[0] == 'run':
            dockerx.run(args.options)
        elif args.command[0] == 'tag':
            dockerx.tag(args.command[1], args.options)
        elif args.command[0] == 'workon':
            dockerx.workon(args.command[1], args.options)
        elif args.command[0] == 'in':
            dockerx.get_into_odoo(args.options)
        else:
            pg, odoo = False, False
            if '--pg' in args.options or '-g' in args.options:
                pg = True
            if '--odoo' in args.options or '-o' in args.options:
                odoo = True
            if '-og' in args.options or '-go' in args.options:
                pg, odoo = True, True
            dockerx.execute(args.command[0], args.options, pg=pg, odoo=odoo)
    if args.command[0] in ('m', 'p'):
        odoox.execute(args.command, args.options)


if __name__ == '__main__':
    main()