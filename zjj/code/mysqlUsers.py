import pymysql


def connect():  # 连接MySQL数据库
    try:
        db = pymysql.connect(
            host="localhost",
            user="root",
            passwd="1561",
            db="users",  # 填写数据库名称
        )
        return db
    except Exception:
        raise Exception("数据库连接失败")


class User:
    def __init__(self):
        self.db = connect()
        cur = self.db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    openid VARCHAR(250),
                    times INT
                    );""")

    def change(self, openid):
        cur = self.db.cursor()

        sql = "SELECT * FROM users WHERE openid = '" + openid + "';"
        cur.execute(sql)
        data = cur.fetchone()
        if data:
            times = data[1] + 1
            sql = "UPDATE users SET times = '" + str(times) + "' WHERE openid = '" + openid + "';"
            cur.execute(sql)
        else:
            times = 1
            sql = "INSERT INTO users VALUES ('" + openid + "', '" + '1' + "');"
            cur.execute(sql)

        self.db.commit()
        cur.close()
        return times
