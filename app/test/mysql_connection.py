import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
import asyncio
from app.module import db_module
# I made a separate directory only for MySQL connection python module


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # The default has changed from selector to proactor in Python 3.8.
    # Thus, this line should be added to detour probable errors


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

        data_input = self.get_argument("message")

        database = db_module.Database()

        database.insert_into_db(data_input)

        self.write("you have saved data :  " + data_input)


class DataSelectHandler(tornado.web.RequestHandler):
    # to get input(id) by HTML and show the allocated data according to what has been input(id)
    def get(self):
        # to show HTML input form by GET method
        self.write('<html><body><form action="/showdata" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        # to get data from Mysql database("mydatabase") and show it on the page "/showdata"
        self.set_header("Content-Type", "text/plain")

        data_input = self.get_argument("message")

        database = db_module.Database()

        value_in_id = database.select_by_id(data_input)

        self.write(value_in_id)


application = tornado.web.Application([
    (r"/", DataInsertHandler),
    (r"/showdata", DataSelectHandler),
    # to map "/" to FormHandler, to map "/showdata" to DataHandler
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)

    socket_address = 8888

    http_server.listen(socket_address)

    # print("the socket address %d has been assigned" % socket_address)
    tornado.ioloop.IOLoop.instance().start()
