from db_conn import DbConn
from traceback import format_exc


class QueryExecutor:

    @staticmethod
    def create_database(db_obj, db_name):
        try:
            db_obj.cur.execute(
                "CREATE DATABASE IF NOT EXISTS {}".format(db_name))
            return "DB chosen"
        except Exception:
            return "db error while creating database"

    @staticmethod
    def use_database(db_obj, db_name):
        try:
            db_obj.cur.execute("USE {}".format(db_name))
            return "DB chosen"
        except Exception as ex:
            print(format_exc())

    @staticmethod
    def drop_table(db_obj, table_name):
        try:
            db_obj.cur.execute("drop table if exists {}".format(table_name))
        except Exception:
            return "db error while dropping table"

    @staticmethod
    def create_table(db_obj, table_name):
        try:
            db_obj.cur.execute("""CREATE TABLE IF NOT EXISTS {}
            (
            Id VARCHAR(100),
            FromAddress VARCHAR(100),
            ToAddress VARCHAR(100),
            MailSub VARCHAR(1000),
            DateReceived BIGINT,
            ReadByUser BOOLEAN,
            Archive BOOLEAN,
            Label Varchar(100),
            PRIMARY KEY (Id)
            )
            """.format(table_name))
        except Exception:
            return "db error while creating table"

    @staticmethod
    def execute_insert_query(db_obj, val):
        try:
            sql = "INSERT INTO HappyMails(Id, FromAddress, ToAddress, MailSub, DateReceived) VALUES (%s, %s, %s, %s, %s)"
            db_obj.cur.executemany(sql, val)
            db_obj.conn.commit()
        except Exception:
            return "db error while inserting values into table"

    @staticmethod
    def execute_select_all_query(db_obj):
        try:
            sql = "Select Id, FromAddress, ToAddress, MailSub, DateReceived, ReadByUser, Archive, Label From HappyMails"
            db_obj.cur.execute(sql)
            all_records = db_obj.cur.fetchall()
            print(
                'Id       , FromAddress       , ToAddress     , MailSub       , DateReceived      , ReadByUser        , Archive       , Label')
            for record in all_records:
                print(record[0][:10], record[1][:10], record[2][:10], record[3][:10].encode('UTF-8'),
                      record[4], record[5], record[6], record[7])
            return all_records
        except Exception as ex:
            print(format_exc())
            return "db error while Selecting all values values from table"
