import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
import asyncio
from app.module import MySQL_conn_Module
# I made a separate directory only for MySQL connection python module


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # The default has changed from selector to proactor in Python 3.8.
    # Thus, this line should be added to detour probable errors


class DataTableShowHandler(tornado.web.RequestHandler):
    # to show data in the schema as a table form
    def get(self):
        columns = MySQL_conn_Module.show_columns_from_table()
        # "contents" has a list of tuples which has table data
        # (ex. : [(id_value1, address_value1), (id_value2, address_value2)...]
        contents = MySQL_conn_Module.select_from_table()

        self.render("bootstrap_table.html",
                    database_name="show table",
                    table_name="Test Table",
                    contents=contents,
                    columns=columns
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
