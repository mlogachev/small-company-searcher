from setuptools import setup, find_packages

setup(
    name='company-cli-tool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
        'psycopg2',
    ],
    entry_points='''
        [console_scripts]
        company_searcher=company_cli_tool.run:do
    '''
)