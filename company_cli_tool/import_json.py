import json
import psycopg2


def import_json(absolute_json_file_path, **dbargs):
    """
    Imports data to Postgres table from json file

    :param str absolute_json_file_path: file path to given json to import
    :keyword str host: Postgres host
    :keyword str port: Postgres port
    :keyword str database: Postgres database
    :keyword str user: Postgres user
    :keyword str password: Postgres password
    """

    with open(absolute_json_file_path, 'r') as fp:
        data = json.load(fp)

    with psycopg2.connect(**dbargs) as conn:
        with conn.cursor() as cur:
            for row in data:
                cur.execute(
                    'INSERT INTO employers (id, parentid, name) '
                    'VALUES (%(id)s, %(ParentId)s, %(Name)s)',
                    row
                )
