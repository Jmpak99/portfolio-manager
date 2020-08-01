import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import sys
import asyncio
from multiprocessing import cpu_count
from enum import Enum
# a separate directory only for MySQL connection python module
from app.module import db_query_module
from controller import get_current_stock_price


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # The default has changed from selector to pro-actor in Python 3.8.
    # Thus, this line should be added to detour probable errors


# to change real column names to readable column names
class ColumnName(Enum):
    TestID = "test_id"
    TestData = "test_data"


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

        data_input = self.get_argument("message").upper()

        # 'contents' has a list of tuples which has table data
        # (ex. : [(test_id1, stock_code1), (test_id2, stock_code2)...]
        contents = db_query_module.select_from_table()

        # if input stock data is not available, it shows error message
        try:
            get_current_stock_price.get_current_price(data_input)

            # get only stock_codes from contents above
            stock_code_list = [stock_code[1] for stock_code in contents]

            # to prevent registering repeated stock code in the db
            existing_data = False
            for x in stock_code_list:
                if x == data_input:
                    existing_data = True

                    self.write("you have already registered {}".format(data_input))
                    break

            if not existing_data:
                db_query_module.insert_into_db(data_input)

                self.write("input stock code has been saved :  " + data_input)

        except IOError as e:
            self.write(str(e))
        except IndexError as e:
            self.write(str(e))
        except RuntimeError as e:
            self.write(str(e))


class DataSelectHandler(tornado.web.RequestHandler):
    # to get input(id) by HTML and show the allocated data according to what has been input(id)
    def get(self):
        # to show HTML input form by GET method
        self.write('<html><body><form action="/show-data" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        # to get data from Mysql database("test_database") and show it on the page "/showdata"
        self.set_header("Content-Type", "text/plain")

        data_input = self.get_argument("message")

        value_in_id = db_query_module.select_by_id(data_input)

        self.write(value_in_id)


class TaskRunner(object):
    executor = ThreadPoolExecutor(max_workers=(cpu_count() * 5))

    @run_on_executor
    def get_stock_price(self, stock_code):
        result = get_current_stock_price.get_current_price(stock_code)

        return result


# to show data in the schema as a table form
class DataTableShowHandler(tornado.web.RequestHandler):
    task_runner = TaskRunner()

    # 'contents' has a list of tuples which has table data
    # (ex. : [(test_id1, stock_code1), (test_id2, stock_code2)...]

    @gen.coroutine
    def get(self):
        contents = db_query_module.select_from_table()

        column_name_list = db_query_module.show_columns_from_table()

        # run get_current_price async threads
        current_stock_price_dict = yield {stock_code[1]: self.task_runner.get_stock_price(stock_code[1])
                                          for stock_code in contents}

        # this is not actual contents in the database table to avoid saving data in the original database
        virtual_contents = [(test_id, stock_code, current_stock_price_dict[stock_code])
                            for test_id, stock_code in contents]

        # readable column list using Enum
        readable_col_list = [ColumnName(col).name for col in column_name_list]

        # this is not an actual column
        virtual_columns = [x for x in readable_col_list]

        virtual_columns.append("Current Stock Price")

        self.render("bootstrap_table.html",
                    database_name="show table",
                    table_name="Test Table",
                    contents=virtual_contents,
                    columns=virtual_columns,
                    )


# to map "/" to FormHandler, to map "/showdata" to DataHandler
# to map "/show-all" to DataTableShowHandler
application = tornado.web.Application([
    (r"/", DataInsertHandler),
    (r"/show-data", DataSelectHandler),
    (r"/show-all", DataTableShowHandler)
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)

    socket_address = 8888
    http_server.listen(socket_address)

    # print("the socket address %d has been assigned" % socket_address)
    tornado.ioloop.IOLoop.instance().start()
