import psycopg2

from collections import deque

SELECT_EMPLOYEES_WITH_IDS_SQL = 'SELECT name FROM employers WHERE id IN %s'
SELECT_CHILDREN_SQL = 'SELECT id FROM employers WHERE parentid = %s'
SELECT_PERSON_SQL = 'SELECT id FROM employers WHERE id = %s'
SELECT_PARENT_ID_SQL = 'SELECT id FROM employers WHERE id = (SELECT parentid FROM employers WHERE id = %s)'


def get_parent_id(cur, person_id):
    result = execute_and_get_result(
        cur,
        SELECT_PARENT_ID_SQL,
        person_id
    )

    return result[0] if result else None


def execute_and_get_result(cursor, query, *params, **kwparams):
    if kwparams:
        cursor.execute(
            query, kwparams
        )
    else:
        cursor.execute(
            query, params
        )

    return cursor.fetchall()


def get_office(person_id):
    with psycopg2.connect(database="company", user="postgres") as conn:
        with conn.cursor() as cur:
            if not execute_and_get_result(cur, SELECT_PERSON_SQL, person_id):
                raise Exception("Does not exists")

            if execute_and_get_result(cur, SELECT_CHILDREN_SQL, person_id):
                raise Exception("Not a person")

            top_node_id = person_id
            parent_id = get_parent_id(cur, top_node_id)
            while parent_id is not None:
                top_node_id = parent_id
                parent_id = get_parent_id(cur, top_node_id)

            queue_of_nodes = deque()
            queue_of_nodes.append(top_node_id)

            office_colleagues = set()
            while queue_of_nodes:
                element_id = queue_of_nodes.popleft()

                new_elements_ids = [
                    row[0]
                    for row in execute_and_get_result(cur, SELECT_CHILDREN_SQL, element_id)
                ]
                if not new_elements_ids:
                    office_colleagues.add(element_id)
                else:
                    for idx in new_elements_ids:
                        queue_of_nodes.append(idx)

            return [
                row[0]
                for row in execute_and_get_result(cur, SELECT_EMPLOYEES_WITH_IDS_SQL, tuple(office_colleagues))
            ]
