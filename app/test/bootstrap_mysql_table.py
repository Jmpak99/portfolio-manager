import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
import asyncio

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.gen import multi
from app.module import db_query_module
from controller import get_current_stock_price


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # The default has changed from selector to pro-actor in Python 3.8.
    # Thus, this line should be added to detour probable errors


class SignupHandler(tornado.web.RequestHandler):
    def __init__(self, application, request):
        # to connect to DB just one time
        self.database = db_query_module.Database()

        super(SignupHandler, self).__init__(application, request)

    def get(self):
        self.write('<html>'
                   '<body>'
                   '<form action="/signup" method="POST">'
                   '<label for="username">ID : </label></br>'
                   '<input type="text" id="user_id" name="user_id"></br>'
                   '<label for="pwd">Password : </label></br>'
                   '<input type="password" id="user_password" name="user_password"></br>'
                   '<input type="submit" value="Submit">'
                   '</form>'
                   '</body>'
                   '</html>'
                   )

    def post(self):
        self.set_header("Content-Type", "text/plain")

        input_id = self.get_argument('user_id')

        input_password = self.get_argument('user_password')

        id_in_db = self.database.select_from_user_info()

        for x in id_in_db:
            if x[0] == input_id:
                return self.write('This ID already exists !')

        self.database.insert_into_user_info(input_id, input_password)

        self.write('you have created your ID : ' + input_id)


# to get data input by html form and transmit input data into MySQL server to save it
class DataInsertHandler(tornado.web.RequestHandler):
    def __init__(self, application, request):
        # to connect to DB just one time
        self.database = db_query_module.Database()

        super(DataInsertHandler, self).__init__(application, request)

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
        contents = self.database.select_from_test_table()

        # if input stock data is not available, it shows error message
        try:
            get_current_stock_price.get_current_price(data_input)

            # get only stock_codes from contents above
            stock_code_list = [stock_code for _, stock_code in contents]

            # to prevent registering repeated stock code in the db
            existing_data = False
            for x in stock_code_list:
                if x == data_input:
                    existing_data = True

                    self.write("you have already registered {}".format(data_input))
                    break

            if not existing_data:
                self.database.insert_into_test_table(data_input)

                self.write("input stock code has been saved :  " + data_input)

        except IOError:
            self.write("stocks object/file was not found or unable to retrieve")
        except IndexError:
            self.write("stock data input was unavailable or not found in Investing.com")
        except RuntimeError:
            self.write("stock data was not found")


# to get input(id) by HTML and show the allocated data according to what has been input(id)
class DataSelectHandler(tornado.web.RequestHandler):
    def __init__(self, application, request):
        self.database = db_query_module.Database()

        super(DataSelectHandler, self).__init__(application, request)

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

        value_in_id = self.database.select_by_id(data_input)

        self.write(value_in_id)


# to show data in the schema as a table form
class DataTableShowHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, executor):
        self.database = db_query_module.Database()

        self.executor = executor

        super(DataTableShowHandler, self).__init__(application, request)

    # get current stock price asynchronously
    # The executor to be used is determined by the executor attributes of self (self.executor)
    @run_on_executor(executor='executor')
    def get_stock_price(self, stock_code):
        result = get_current_stock_price.get_current_price(stock_code)
        return result

    async def get(self):
        # 'contents' has a list of tuples which has table data
        # (ex. : [(test_id1, stock_code1), (test_id2, stock_code2)...]
        contents = self.database.select_from_test_table()

        column_name_list = self.database.show_columns_from_test_table()

        # run get_current_price async threads and wait for future objects until they are loaded
        current_stock_price_dict = await multi({stock_code: self.get_stock_price(stock_code)
                                                for _, stock_code in contents})

        # this is not actual contents in the database table to avoid saving data in the original database
        virtual_contents = [(test_id, stock_code, current_stock_price_dict[stock_code])
                            for test_id, stock_code in contents]

        await self.render("bootstrap_table.html",
                          database_name="show table",
                          table_name="Test Table",
                          contents=virtual_contents,
                          )


if __name__ == "__main__":
    executor = ThreadPoolExecutor(max_workers=4)

    # to map "/" to FormHandler, to map "/showdata" to DataHandler
    # to map "/show-all" to DataTableShowHandler
    application = tornado.web.Application([
        (r"/", DataInsertHandler),
        (r"/show-data", DataSelectHandler),
        (r"/show-all", DataTableShowHandler, dict(executor=executor)),
        (r"/signup", SignupHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(application)

    socket_address = 8888
    http_server.listen(socket_address)

    tornado.ioloop.IOLoop.instance().start()
