import argparse
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument('command', nargs="*")
parser.add_argument('options', nargs=argparse.REMAINDER)

args = parser.parse_args()

subprocess.run(args.command + args.options) 
