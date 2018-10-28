#!/usr/bin/env python

import click
import os

from company_cli_tool.import_json import import_json
from company_cli_tool.get_office import get_office


@click.command('import')
@click.argument('json_file')
@click.option('--host', '-h', default='localhost', help='Postgres host')
@click.option('--port', '-p', default='5432', help='Postgres port')
@click.option('--database', '-d', default='company', help='Postgres database name')
@click.option('--user', '-u', default='postgres', help='Postgres user')
@click.option('--password', '-w', default='', help='Postgres user password')
def run_import(json_file, **kwargs):
    fp = os.path.join(os.getcwd(), json_file)
    import_json(fp, **kwargs)


@click.command('office')
@click.argument('user_id')
@click.option('--host', '-h', default='localhost', help='Postgres host')
@click.option('--port', '-p', default='5432', help='Postgres port')
@click.option('--database', '-d', default='company', help='Postgres database name')
@click.option('--user', '-u', default='postgres', help='Postgres user')
@click.option('--password', '-w', default='', help='Postgres user password')
def run_get_office(user_id, **kwargs):
    print(' '.join(get_office(int(user_id), **kwargs)))


@click.group('do')
def do():
    pass


do.add_command(run_import)
do.add_command(run_get_office)
