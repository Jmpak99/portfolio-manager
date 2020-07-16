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

def insert_into_db(data_input):
    # MySQL INSERT function
    db_class = Database()

    sql = "INSERT INTO test_table (test_data) VALUES (%s)"

    val = (data_input,)

    db_class.execute(sql, val)
    #insert input data into test_data
    #structure (schema : 'mydatabase' -> table : 'test_table' -> column : 'test_data')
    db_class.commit()
    #to apply changes and commit
    print(db_class.mycursor.rowcount, "record inserted.")


def select_by_id(id_input):
    # when id number is input, it returns data matched to the input id using MySQL SELECT function
    db_class = Database()

    sql = "SELECT * FROM test_table WHERE test_id = %s"

    id = (id_input,)

    db_class.execute(sql, id)

    row = db_class.mycursor.fetchall()
    value_in_id = row[0][1]
    #row structure --> [(x, y)] tuple in list, so I refered to y by row[0][1]

    return value_in_id

