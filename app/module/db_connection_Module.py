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

    def execute(self, query, args={}):
        self.mycursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.mycursor.execute(query, args)
        row = self.mycursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.mycursor.execute(query, args)
        row = self.mycursor.fetchall()
        return row

    def commit(self):
        self.cnx.commit()