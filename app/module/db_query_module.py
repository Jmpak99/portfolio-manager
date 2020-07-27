import mysql.connector
from enum import Enum


class Database(object):
    def __init__(self):
        # to connect mysql_database
        self.cnx = mysql.connector.connect(
            # connect to mysql server
            host='127.0.0.1',
            password='1111',
            user='root',
            port=3306,
            database='test_database'
        )
        self.mycursor = self.cnx.cursor()

    def execute(self, query, args=None):
        self.mycursor.execute(query, args)

    def execute_one(self, query, args=None):
        self.mycursor.execute(query, args)
        row = self.mycursor.fetchone()
        return row

    def execute_all(self, query, args=None):
        self.mycursor.execute(query, args)
        row = self.mycursor.fetchall()
        return row

    def commit(self):
        self.cnx.commit()

    def insert_into_db(self, data_input):
        # MySQL INSERT function
        db_class = Database()

        sql = "INSERT INTO test_table (test_data) VALUES (%s)"

        val = (data_input,)
        # In Python, a tuple containing a single value must include a comma.
        # For example, ('abc') is evaluated as a scalar while ('abc',) is evaluated as a tuple.
        db_class.execute(sql, val)
        # insert input data into test_data
        # structure (schema : 'mydatabase' -> table : 'test_table' -> column : 'test_data')

        db_class.commit()

    def select_by_id(self, id_input):
        # when id number is input, it returns data matched to the input id using MySQL SELECT function
        db_class = Database()

        sql = "SELECT * FROM test_table WHERE test_id = %s"

        id = (id_input,)

        db_class.execute(sql, id)

        row = db_class.mycursor.fetchall()

        value_in_id = row[0][1]
        # row structure --> [(x, y)] tuple in list, so I referred to y by row[0][1]

        return value_in_id


def show_columns_from_table():
    # to take a name of the each column from the table
    db_class = Database()

    sql = "SHOW COLUMNS FROM test_table"

    db_class.execute(sql)

    rows = db_class.mycursor.fetchall()

    columns = [row[0] for row in rows]
    # list comprehension used

    return columns
    # to return name of each column as a list


def select_from_table():
    # to get all table record data by SELECT method
    db_class = Database()

    sql = "SELECT test_id, test_data FROM test_table"

    db_class.execute(sql)

    row = db_class.mycursor.fetchall()

    return row

