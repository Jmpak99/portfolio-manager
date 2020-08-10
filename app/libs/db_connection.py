import mysql.connector


class Database(object):
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='127.0.0.1',
            password='1111',
            user='root',
            port=3306,
            database='test_database'
        )

    def insert_into_test_table(self, data_input):
        '''DEPRECATED This function will be deleted in the next PR'''
        cursor = self.conn.cursor()

        sql = "INSERT INTO test_table (test_data) VALUES (%s)"

        val = (data_input,)

        cursor.execute(sql, val)
        # insert input data into test_data
        # structure (schema : 'test_database' -> table : 'test_table' -> column : 'test_data')

        self.conn.commit()

    def select_from_test_table(self):
        '''DEPRECATED This functions will be deleted in the next PR'''

        cursor = self.conn.cursor()

        sql = "SELECT test_id, test_data FROM test_table"

        cursor.execute(sql)

        row = cursor.fetchall()
        return row
