import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
import asyncio
import mysql.connector

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # The default has changed from selector to proactor in Python 3.8.
    # Thus, this line should be added to detour probable errors


class FormHandler(tornado.web.RequestHandler):
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

        data_raw = self.request.body.decode('utf-8')
        data_splited = data_raw.split("=")
        data_input = data_splited[1]
        # to change Bytes type into Str
        # to take only value by splitting it

        self.write("you have saved data :  " + data_input + "  to MySQL server 'mydatabase'")


        cnx = mysql.connector.connect(
        # connect to mysql server
            host='127.0.0.1',
            password='your_password',
            user='root',
            port=3307,
            ##port number default is '3306', but in my computer 3306 makes error so I assigned it to '3307'
            database='mydatabase'
            #database name is "mydatabase"
        )

        mycursor = cnx.cursor()

        sql = "INSERT INTO test_table (test_data) VALUES (%s)"
        val = (data_input,)
        mycursor.execute(sql, val)
        #insert input data into test_data
        #structure (schema : 'mydatabase' -> table : 'test_table' -> column : 'test_data')
        cnx.commit()
        #to apply changes and commit
        print(mycursor.rowcount, "record inserted.")


class DataHandler(tornado.web.RequestHandler):
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

        data_raw = self.request.body.decode('utf-8')
        data_splited = data_raw.split("=")
        data_input = data_splited[1]
        #to change bytes type to string type

        cnx = mysql.connector.connect(
            #connect to mysql server
            host='127.0.0.1',
            password='um8910vs',
            user='root',
            port=3307,
            database='mydatabase'
        )

        mycursor = cnx.cursor()

        sql = "SELECT * FROM test_table WHERE test_id = %s"
        id = (data_input,)
        mycursor.execute(sql, id)
        #only show test_table values according to test_id which has been input on the "/showdata" page

        myresult = mycursor.fetchall()
        import itertools
        out = list(itertools.chain(*myresult))
        #change tupel to list
        id_value = out[1]
        #out[0] is input id and out[1] is the value of it
        self.write(id_value)
        #to write data in "mydatabase" matched to input id

application = tornado.web.Application([
    (r"/", FormHandler), (r"/showdata", DataHandler),
    #to map "/" to FormHandler, to map "/showdata" to DataHandler
])



if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    socket_address = 8888
    http_server.listen(socket_address)

    print("the socket address %d has been assigned" % socket_address)
    tornado.ioloop.IOLoop.instance().start()





