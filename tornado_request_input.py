import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # The default has changed from selector to proactor in Python 3.8.
    # Thus, this line should be added to detour probable errors


class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        # to request by "GET" method
        self.write('<html><body><form action="/myform" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
        # write HTML, making a space for input("text" form) and a button
        # if you click the button, it requests to "/myform" by "POST" method
        # to do this you need a handler which includes "POST" function and this is in the following line

    def post(self):
        # to request to "/myform" by "POST" method
        self.set_header("Content-Type", "text/plain")
        # to set the type of text which has been input in the "/" page and will be shown in the "/myform" address
        self.write("You wrote " + self.get_body_argument("message"))
        # to show what has been written in the "/"page
        # get_body_argument will get argument in the body of MyformHandler as a string type


application = tornado.web.Application([
    (r"/", MyFormHandler)
])
# this set of (r"url", handler) is called "route", it proceeds to run a web server

if __name__ == "__main__":
    # It works only when the current process is main
    http_server = tornado.httpserver.HTTPServer(application)
    # to start a non-blocking, single threaded server
    socket_address = 8888
    http_server.listen(socket_address)
    # .listen() initializes simple single process

    print("the socket address %d has been assigned" % socket_address)
    tornado.ioloop.IOLoop.instance().start()
    # to start a current IOloop

