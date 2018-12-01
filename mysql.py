import pymysql
from datetime import datetime as dt


class MySQL(object):
    def __init__(self):
        self.error = None
        try:
            self.connection = pymysql.connect(host='localhost',
                                              user='root',
                                              password='pass1122333',
                                              db='twitter_db',
                                              charset='utf8mb4')
        except:
            raise Exception('fail to connect to mysql.')

    def mysql_log(self, log_record='Unknown'):
        if self.error:
            log_record = str(self.error)
        try:
            with self.connection.cursor() as cursor:
                sql = "insert into `mysql_data`(`time`,`record`) values(%s,%s)"
                cursor.execute(sql, (dt.now(), log_record))
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            self.connection.close()
            raise Exception

    def save_label(self, username, label, url):
        try:
            with self.connection.cursor() as cursor:
                sql = "insert into `mysql_label`(`twitter_id`, `label`,`img_url` ) values(%s, %s, %s)"
                cursor.execute(sql, (username, label, url))
                self.connection.commit()
        except Exception:
            self.error = Exception
            # self.mysql_log()
            self.connection.close()
            raise Exception

    def mysql_search(self, key):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM mysql_label WHERE label like "%{}%"'.format(key))
                results = cursor.fetchall()
        except Exception:
            self.error = Exception
            self.connection.close()
            raise Exception
        finally:
            self.mysql_log('Search {} in mysql_label.'.format(key))
        user_list = []
        for row in results:
            if not row[0] in user_list:
                user_list.append(row[0])
        return user_list

    def mysql_statistics(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT COUNT(*) FROM mysql_data')
                result = cursor.fetchone()
        except Exception as e:
            self.error = e
            self.connection.close()
            raise e
        finally:
            self.mysql_log('Count logs in mysql_data.')
        return result