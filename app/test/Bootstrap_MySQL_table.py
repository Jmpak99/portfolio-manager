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

    for row in rows:
        columns.append(row[0])
        # to save column name in the "columns" list
    return columns


class DataTableShowHandler(tornado.web.RequestHandler):
    # to show data in the schema as a table form
    def get(self):
        columns = show_columns_from_table()
        # "contents" has a list of tuples which has table data
        # (ex. : [(id_value1, address_value1), (id_value2, address_value2)...]
        contents = select_from_table()

        self.render("bootstrap_table.html",
                    database_name = "show table",
                    table_name = "Test Table",
                    contents = contents,
                    columns = columns
                    )

application = tornado.web.Application([
    (r"/show-all", DataTableShowHandler)
    #to map "/" to FormHandler, to map "/showdata" to DataHandler
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)

    socket_address = 8888

    http_server.listen(socket_address)
    #print("the socket address %d has been assigned" % socket_address)
    tornado.ioloop.IOLoop.instance().start()
