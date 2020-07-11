import mysql.connector

cnx = mysql.connector.connect(
    host='127.0.0.1',
    password='um8910vs',
    user='root',
    port=3307,
    database='mydatabase'
    )

mycursor = cnx.cursor()


sql = "INSERT INTO test_table (test_data) VALUES (%s)"
val =
mycursor.execute(sql, val)


for x in mycursor:
    print(x)




