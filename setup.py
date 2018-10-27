from setuptools import setup

setup(
    name='company_searcher',
    version='0.1',
    pymodules=['run'],
    install_requires=[
        'Click',
        'psycopg2',
    ],
    entry_points='''
        [console_scripts]
        company_searcher=run:do
    '''
)