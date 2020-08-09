from app.libs import db_connection


class TableStockCode(object):
    def __init__(self):
        self.conn = db_connection.Database().conn

    def add_stock_code(self, data_input):
        cursor = self.conn.cursor()

        sql = "INSERT INTO stock_code (stock_code) VALUES (%s)"

        val = (data_input,)

        cursor.execute(sql, val)
        # insert input data into test_data
        # structure (schema : 'test_database' -> table : 'test_table' -> column : 'test_data')

        self.conn.commit()

    # to get all table record data by SELECT method
    def select_from_table(self):
        cursor = self.conn.cursor()

        sql = "SELECT id, stock_code FROM stock_code"

        cursor.execute(sql)

        row = cursor.fetchall()
        return row

