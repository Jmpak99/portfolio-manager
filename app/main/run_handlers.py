import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
import asyncio
import settings

from concurrent.futures import ThreadPoolExecutor
from app.stock.handlers.stock_handlers import DataTableShowHandler, DataInsertHandler


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # The default has changed from selector to pro-actor in Python 3.8.
    # Thus, this line should be added to detour probable errors


if __name__ == "__main__":
    executor = ThreadPoolExecutor(max_workers=4)

    settings = {"template_path": settings.TEMPLATE_PATH,
                "static_path": settings.STATIC_PATH}

    application = tornado.web.Application([
        (r"/", DataInsertHandler),
        (r"/show-all", DataTableShowHandler, dict(executor=executor)),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)

    socket_address = 8888
    http_server.listen(socket_address)

    tornado.ioloop.IOLoop.instance().start()
