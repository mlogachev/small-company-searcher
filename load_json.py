import json
import psycopg2


def import_json(absolute_json_file_path):
    """
    Imports data to Postgres table
    :param str absolute_json_file_path: file path to given json to import
    """

    with open(absolute_json_file_path, 'r') as fp:
        data = json.load(fp)

    with psycopg2.connect(database="company", user="postgres") as conn:
        with conn.cursor() as cur:
            for row in data:

                if row['ParentId'] is not None:
                    cur.execute(
                        'SELECT OfficeId FROM employers WHERE id=%s',
                        (row['ParentId'],)
                    )
                    row['OfficeId'] = cur.fetchone()[0]

                    cur.execute(
                        'UPDATE employers SET person = FALSE WHERE id = %s',
                        (row['ParentId'],)
                    )
                else:
                    row['OfficeId'] = row['id']

                cur.execute(
                    'INSERT INTO employers (id, parentid, name, officeid) '
                    'VALUES (%(id)s, %(ParentId)s, %(Name)s, %(OfficeId)s)',
                    row
                )


if __name__ == '__main__':
    import_json("/Users/MikhailLogachev/Development/tensor_test_task/data.json")
