from app.libs import db_connection


class TableUserInfo(object):
    def __init__(self):
        self.conn = db_connection.Database().conn

    # columns : id(PRIMARY KEY), user_id VARCHAR(30), user_password VARCHAR(45)
    def add_user_info(self, input_id, input_password):
        cursor = self.conn.cursor()

        sql = "INSERT INTO user_info (user_id, user_password) VALUES (%s, %s)"

        val = (input_id, input_password)

        cursor.execute(sql, val)

        self.conn.commit()

    def select_from_table(self):
        cursor = self.conn.cursor()

        sql = "SELECT user_id FROM user_info"

        cursor.execute(sql)

        row = cursor.fetchall()
        return row
