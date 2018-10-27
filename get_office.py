import psycopg2


def get_office(person_id):
    with psycopg2.connect(database="company", user="postgres") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT name "
                "FROM employers "
                "WHERE "
                "person = TRUE AND "
                "officeid = (SELECT officeid from employers WHERE id = %s)",
                (person_id,)
            )

            rows = cur.fetchall()
            return [row[0] for row in rows]


if __name__ == '__main__':
    get_office(3)
