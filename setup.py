import os

from setuptools import setup, find_packages


def install_required():
    with open(os.path.join(os.path.dirname(__file__), 'requirement.txt'), 'r') as f:
        return list(f.readlines())


setup(
    name='company-cli-tool',
    version='0.1',
    packages=find_packages(),
    install_requires=install_required(),
    entry_points='''
        [console_scripts]
        com-cli-tool=company_cli_tool.run:do
    '''
)
