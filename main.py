import argparse
import subprocess

from odoox import Odoox

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
else:
    pg, odoo = False, False
    if '--pg' in args.options or '-g' in args.options:
        pg = True
    if '--odoo' in args.options or '-o' in args.options:
        odoo = True
    if '-og' in args.options or '-go' in args.options:
        pg, odoo = True, True
    odoox.execute(args.command[0], args.options, pg=pg, odoo=odoo)
