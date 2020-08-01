import mysql.connector


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

    def insert_into_db(self, data_input):
        # MySQL INSERT function
        cursor = self.cnx.cursor()

        sql = "INSERT INTO test_table (test_data) VALUES (%s)"

        val = (data_input,)

        cursor.execute(sql, val)
        # insert input data into test_data
        # structure (schema : 'mydatabase' -> table : 'test_table' -> column : 'test_data')

        self.cnx.commit()

    def select_by_id(self, id_input):
        # when id number is input, it returns data matched to the input id using MySQL SELECT function
        cursor = self.cnx.cursor()

        sql = "SELECT * FROM test_table WHERE test_id = %s"

        id = (id_input,)

        cursor.execute(sql, id)

        row = cursor.fetchall()

        value_in_id = row[0][1]
        # row structure --> [(x, y)] tuple in list, so I referred to y by row[0][1]

        return value_in_id

    def show_columns_from_table(self):
        # to take a name of the each column from the table
        cursor = self.cnx.cursor()

        sql = "SHOW COLUMNS FROM test_table"

        cursor.execute(sql)

        rows = cursor.fetchall()

        columns = [row[0] for row in rows]
        # list comprehension used

        return columns
        # to return name of each column as a list

    def select_from_table(self):
        # to get all table record data by SELECT method
        cursor = self.cnx.cursor()

        sql = "SELECT test_id, test_data FROM test_table"

        cursor.execute(sql)

        row = cursor.fetchall()

        return row
