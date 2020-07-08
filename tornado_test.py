import tornado.ioloop
import tornado.web
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # The default has changed from selector to proactor in Python 3.8.
    # Thus, this line should be added to detour probable error


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # "get" function has been added by means of class inheritance from "tornado.web.RequestHandler"
        # to post "Hello, world!" to the HTTP server (not sure if this is actually 'get' or 'post')
        self.write("Hello, world!")


def make_app():
    # to make a function to read "MainHandler" (not sure... please add some comment)
    return tornado.web.Application([
        # A collection of request handlers that make up a web application and can be passed to HTTPSever directly
        (r"/", MainHandler),
        # URL "/" is being mapped on "MainHandler"
    ])


if __name__ == "__main__":
    # the commands below only work when this module is the main program
    app = make_app()
    # to assign the value of "make_app()" to "app"
    app.listen(8888)
    # Starts an HTTP server for this application on the given port(8888)
    # It returns HTTPSever object
    tornado.ioloop.IOLoop.current().start()
