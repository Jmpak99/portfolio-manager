import mysql.connector


class Database():
    def __init__(self):
        # to connect mysql_database
        self.cnx = mysql.connector.connect(
            # connect to mysql server
            host='127.0.0.1',
            password='your_password',
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

    columns = show_columns_from_table()

    column = ""
    # I don't know whether convention of empty string designation is "" or "None"
    for x in columns:
        column = column + x + ","

    column = column.rstrip(",")
    # to erase "," at the end
    sql = "SELECT %s FROM test_table" %column
    # to use actual column names directly in the query statement instead of using "*"
    # 'column' could have several columns --> ex) "test_id,test_data"
    db_class.execute(sql)

    row = db_class.mycursor.fetchall()

    return row