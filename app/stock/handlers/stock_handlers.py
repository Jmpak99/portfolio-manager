import tornado.web

from tornado.concurrent import run_on_executor
from tornado.gen import multi
from app.libs import db_connection
from app.stock.controller import get_current_stock_price


# to get data input by html form and transmit input data into MySQL server to save it
class DataInsertHandler(tornado.web.RequestHandler):
    def __init__(self, application, request):
        self.database = db_connection.Database()

        super(DataInsertHandler, self).__init__(application, request)

    def get(self):
        self.write('<html><body><form action="/" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")

        data_input = self.get_argument("message").upper()

        # 'contents' has a list of tuples which has table data
        # (ex. : [(test_id1, stock_code1), (test_id2, stock_code2)...]
        contents = self.database.select_from_test_table()

        # if input stock data is not available, it shows error message
        current_price = get_current_stock_price.get_current_price(data_input)

        # if current_price is successfully received without errors, it returns float type
        # otherwise, it returns (status=False, error_msg)
        if type(current_price) == tuple:
            error_msg = current_price[1]
            self.write(error_msg)
            return
        else:
            pass

        # get only stock_codes from contents above
        stock_code_list = [stock_code for _, stock_code in contents]

        # prevent registering repeated stock code in the db
        existing_data = False
        for x in stock_code_list:
            if x == data_input:
                existing_data = True

                self.write("you have already registered {}".format(data_input))
                break

        if not existing_data:
            self.database.insert_into_test_table(data_input)

            self.write("input stock code has been saved :  " + data_input)


class DataTableShowHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, executor):
        self.database = db_connection.Database()

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

        # run get_current_price async threads and wait for future objects until they are loaded
        current_stock_price_dict = await multi({stock_code: self.get_stock_price(stock_code)
                                                for _, stock_code in contents})

        # this is not actual contents in the database table to avoid saving data in the original database
        virtual_contents = [(test_id, stock_code, current_stock_price_dict[stock_code])
                            for test_id, stock_code in contents]

        return self.render("C:\\Users\\Administrator\\PycharmProjects\\portfolio-manager\\templates\\bootstrap_table"
                           ".html",
                           database_name="show table",
                           table_name="Test Table",
                           contents=virtual_contents,
                           )
