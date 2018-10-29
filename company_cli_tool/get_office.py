import psycopg2

from collections import deque

from .exceptions import QueryException

SELECT_EMPLOYEES_WITH_IDS_SQL = 'SELECT name FROM employers WHERE id IN %s'
SELECT_CHILDREN_IDS_SQL = 'SELECT id FROM employers WHERE parentid = %s'
SELECT_PERSON_ID_SQL = 'SELECT id FROM employers WHERE id = %s'
SELECT_PARENT_ID_SQL = 'SELECT parentid FROM employers WHERE id = %s'


def get_parent_id(cursor, person_id):
    """
    Returns parent id of given element
    :param cursor: current cursor
    :param int person_id: given person id
    :return int|None: 
    """
    result = execute_and_get_result(
        cursor,
        SELECT_PARENT_ID_SQL,
        person_id
    )

    return result[0][0] if result else None


def execute_and_get_result(cursor, query, *params, **kwparams):
    """
    Executre given query using cursor, and return all resulted rows

    :param cursor: cursor to given connection
    :param query: SQL-string to execute
    :param params: non keyword params, must supply either params, or kwparams
    :param kwparams: keyword params, must supply either params, or kwparams
    :return: results of query
    """
    if kwparams and params:
        raise Exception("Pass either params or keyword params, not both")

    if kwparams:
        cursor.execute(
            query, kwparams
        )
    else:
        cursor.execute(
            query, params
        )

    return cursor.fetchall()


def get_office(person_id, **dbargs):
    """
    Find all colleagues of given person, working in the same office
    Assumptions are:
        - Office is a row in table, which does not have parent
        - Person is a row in table, which does not have children
        - Anything else is a department

    :param int person_id: id of person in postgres table
    :keyword str host: Postgres host
    :keyword str port: Postgres port
    :keyword str database: Postgres database
    :keyword str user: Postgres user
    :keyword str password: Postgres password
    """
    with psycopg2.connect(**dbargs) as conn:
        with conn.cursor() as cur:
            if not execute_and_get_result(cur, SELECT_PERSON_ID_SQL, person_id):
                raise QueryException("Record with id {} does not exists".format(person_id))

            if execute_and_get_result(cur, SELECT_CHILDREN_IDS_SQL, person_id):
                raise QueryException("Record with id {} is not a person".format(person_id))

            top_node_id = person_id
            parent_id = get_parent_id(cur, top_node_id)
            while parent_id is not None:
                top_node_id = parent_id
                parent_id = get_parent_id(cur, top_node_id)

            queue_of_nodes = deque()
            queue_of_nodes.append(top_node_id)

            office_colleagues_ids = set()
            while queue_of_nodes:
                element_id = queue_of_nodes.popleft()

                new_elements_ids = [
                    row[0]
                    for row in execute_and_get_result(cur, SELECT_CHILDREN_IDS_SQL, element_id)
                ]
                if not new_elements_ids:
                    office_colleagues_ids.add(element_id)
                else:
                    for idx in new_elements_ids:
                        queue_of_nodes.append(idx)

            return [
                row[0]
                for row in execute_and_get_result(cur, SELECT_EMPLOYEES_WITH_IDS_SQL, tuple(office_colleagues_ids))
            ]
