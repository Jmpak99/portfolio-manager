import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
import asyncio
from app.module import dbModule
# I made a separate directory only for MySQL connection python module


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # The default has changed from selector to proactor in Python 3.8.
    # Thus, this line should be added to detour probable errors


def insert_into_db(data_input):
    # MySQL INSERT function
    db_class = dbModule.Database()

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
    db_class = dbModule.Database()

    sql = "SELECT * FROM test_table WHERE test_id = %s"

    id = (id_input,)

    db_class.execute(sql, id)

    row = db_class.mycursor.fetchall()
    value_in_id = row[0][1]
    #row structure --> [(x, y)] tuple in list, so I refered to y by row[0][1]

    return value_in_id


def select_from_table():
    # to get all table record data by SELECT method
    db_class = dbModule.Database()

    sql = "SELECT * FROM test_table"

    db_class.execute(sql)

    row = db_class.mycursor.fetchall()
    return row

def show_columns_from_table():
    # to take a name of the each column from the table
    db_class = dbModule.Database()

    sql = "SHOW COLUMNS FROM test_table"

    db_class.execute(sql)

    rows = db_class.mycursor.fetchall()

    columns = []

    print (rows)
    for row in rows:
        columns.append(row[0])
        # to save column name in the "columns" list
    return columns

class DataInsertHandler(tornado.web.RequestHandler):
# to get data input by html form and transmit input data into MySQL server to save it
    def get(self):
        # to request an input form by GET method
        self.write('<html><body><form action="/" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
        # input data moves to "/" by POST method

    def post(self):
        self.set_header("Content-Type", "text/plain")
        # to set header type

        data_input = self.get_argument("message")

        insert_into_db(data_input)

        self.write("you have saved data :  " + data_input + "  to MySQL server 'mydatabase'")


class DataSelectHandler(tornado.web.RequestHandler):
    #to get input(id) by HTML and show the allocated data according to what has been input(id)
    def get(self):
        #to show HTML input form by GET method
        self.write('<html><body><form action="/showdata" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')


    def post(self):
        #to get data from Mysql database("mydatabase") and show it on the page "/showdata"
        self.set_header("Content-Type", "text/plain")

        data_input = self.get_argument("message")

        value_in_id = select_by_id(data_input)

        self.write(value_in_id)


class DataTableShowHandler(tornado.web.RequestHandler):
    # to show data in the schema as a table form
    def get(self):
        columns = show_columns_from_table()
        # "contents" has a list of tuples which has table data
        # (ex. : [(id_value1, address_value1), (id_value2, address_value2)...]
        contents = select_from_table()

        self.render("bootstrap_test.html",
                    database_name = "show table",
                    table_name = "Test Table",
                    contents = contents,
                    columns = columns
                    )


application = tornado.web.Application([
    (r"/", DataInsertHandler),
    (r"/showdata", DataSelectHandler),
    (r"/show-all", DataTableShowHandler)
    #to map "/" to FormHandler, to map "/showdata" to DataHandler
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    socket_address = 8888
    http_server.listen(socket_address)

    #print("the socket address %d has been assigned" % socket_address)
    tornado.ioloop.IOLoop.instance().start()





