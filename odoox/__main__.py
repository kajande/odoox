import argparse
import subprocess

from odoox import Odoox
from odoox import modules

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', nargs="*")
    parser.add_argument('options', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    odoox = Odoox()

    if args.command[0] == 'docker':
        subprocess.run(args.command + args.options)
    elif args.command[0] == 'build':
        odoox.build(args.options)
    elif args.command[0] == 'run':
        odoox.run(args.options)
    elif args.command[0] == 'tag':
        odoox.tag(args.command[1], args.options)
    elif args.command[0] == 'workon':
        odoox.workon(args.command[1], args.options)
    elif args.command[0] == 'in':
        odoox.get_into_odoo(args.options)
    elif args.command[0] == 'm':
        modules.execute(args.command[1:], args.options)
    else:
        pg, odoo = False, False
        if '--pg' in args.options or '-g' in args.options:
            pg = True
        if '--odoo' in args.options or '-o' in args.options:
            odoo = True
        if '-og' in args.options or '-go' in args.options:
            pg, odoo = True, True
        odoox.execute(args.command[0], args.options, pg=pg, odoo=odoo)

if __name__ == '__main__':
    main()