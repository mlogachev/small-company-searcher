#!/usr/bin/env python

import click
import os

from import_json import import_json
from get_office import get_office


@click.command('import')
@click.argument('json_file')
@click.option('--db', default='company', help='Postgres database name')
@click.option('--user', default='postgres', help='Postgres user')
def run_import(json_file, db, user):
    fp = os.path.abspath(os.path.join(os.path.dirname(__file__), json_file))
    import_json(fp, database=db, user=user)


@click.command('office')
@click.argument('user_id')
@click.option('--db', default='company', help='Postgres database name')
@click.option('--user', default='postgres', help='Postgres user')
def run_get_office(user_id, db, user):
    print(get_office(int(user_id)))


@click.group('do')
def do():
    pass


do.add_command(run_import)
do.add_command(run_get_office)
