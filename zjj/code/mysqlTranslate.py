import pymysql


def connect():  # 连接MySQL数据库
    try:
        db = pymysql.connect(
            host="localhost",  # 主机地址，默认
            user="root",  # 用户名
            passwd="1561",  # 密码
            db="zjj",  # 填写数据库名称
        )
        return db
    except Exception:
        raise Exception("数据库连接失败")


class Tran:
    def __init__(self):
        self.db = connect()
        cur = self.db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS dictionary(
                    language VARCHAR(25),
                    Chinese  VARCHAR(25),
                    foreignLanguage  VARCHAR(25)
                    );""")  # 如果表不存在，则创建

    def tra(self, sou, tar, word):  # 翻译，三个参数分别为’源语种‘，’目标语种‘，’单词‘
        cur = self.db.cursor()
        if sou != '中文':
            cur.execute("SELECT Chinese FROM dictionary WHERE language = '"
                        + sou + "' AND foreignLanguage = '" + word + "';")  # 如果单词不是中文，找到单词对应的中文
            word = cur.fetchone()[0]
        if tar != '中文':
            cur.execute("SELECT foreignLanguage FROM dictionary WHERE language = '"
                        + tar + "' AND Chinese = '" + word + "';")  # 中文翻译成目标语种
            re = cur.fetchone()[0]
        else:
            re = word
        cur.close()
        return re

    def ins(self, tar, word1, word2):
        cur = self.db.cursor()
        sql = "SELECT * FROM dictionary WHERE language = '" \
              + tar + "' AND Chinese = '" + word1 + "';"
        cur.execute(sql)
        data = cur.fetchone()
        if data:
            re = '重复添加'
        else:
            sql = "INSERT INTO dictionary VALUES ('" \
                  + tar + "', '" + word1 + "', '" + word2 + "');"
            cur.execute(sql)
            re = '添加成功'
        self.db.commit()
        cur.close()
        return re
