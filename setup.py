from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name='Odoox',
    description="Odoo dev automation tool",
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'odoox = odoox.__main__:main'
        ]
    },
    author="Moctar Diallo",
    author_email="moctar.diallo@kajande.com",
    url="https://github.com/kajande/odoox",
)