import psycopg2

from collections import deque


def get_parent_id(cur, person_id):
    result = execute_and_get_result(
        cur,
        'SELECT id FROM employers WHERE id = (SELECT parentid FROM employers WHERE id = %s)',
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
            select_person = 'SELECT id FROM employers WHERE id = %s'
            select_children = 'SELECT id FROM employers WHERE parentid = %s'

            if not execute_and_get_result(cur, select_person, person_id):
                raise Exception("Does not exists")

            if execute_and_get_result(cur, select_children, person_id):
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
                    for row in execute_and_get_result(cur, select_children, element_id)
                ]
                if not new_elements_ids:
                    office_colleagues.add(element_id)
                else:
                    for idx in new_elements_ids:
                        queue_of_nodes.append(idx)

            sql = 'SELECT name FROM employers WHERE id IN %s'
            return [row[0] for row in execute_and_get_result(cur, sql, tuple(office_colleagues))]
