import mysql.connector


class Database():
    def __init__(self):
        # to connect mysql_database
        self.cnx = mysql.connector.connect(
            # connect to mysql server
            host='127.0.0.1',
            password='um8910vs',
            user='root',
            port=3307,
            database='mydatabase'
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

class db_Table():
    def select_from_table(self):
        # to get all table record data by SELECT method
        db_class = Database()

        sql = "SELECT * FROM test_table"

        db_class.execute(sql)

        row = db_class.mycursor.fetchall()

        return row


    def show_columns_from_table(self):
        # to take a name of the each column from the table
        db_class = Database()

        sql = "SHOW COLUMNS FROM test_table"

        db_class.execute(sql)

        rows = db_class.mycursor.fetchall()

        columns = []

        for row in rows:
            columns.append(row[0])
            # to save column name in the "columns" list
        return columns
