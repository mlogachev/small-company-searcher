import json
import psycopg2


def import_json(absolute_json_file_path, database, user):
    """
    Imports data to Postgres table
    :param str absolute_json_file_path: file path to given json to import
    :param str database: database name, defaults to "company"
    :param str user: database user, defaults to "postgres"
    """

    with open(absolute_json_file_path, 'r') as fp:
        data = json.load(fp)

    with psycopg2.connect(**dict(database=database, user=user)) as conn:
        with conn.cursor() as cur:
            for row in data:
                cur.execute(
                    'INSERT INTO employers (id, parentid, name) '
                    'VALUES (%(id)s, %(ParentId)s, %(Name)s)',
                    row
                )


if __name__ == '__main__':
    import_json("/Users/MikhailLogachev/Development/tensor_test_task/data.json", database="company", user="postgres")
