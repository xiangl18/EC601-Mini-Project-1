import pymongo
from datetime import datetime as dt

class MongoDB(object):
    def __init__(self):
        try:
            mongoDB = pymongo.MongoClient('mongodb://localhost:27017/')
            self.mongodb = mongoDB['twitter_database']
        except Exception:
            log_record = 'fail to connect to MongoDB. Error: {}'.format(str(Exception))
            MongoDB.mongodb_log(log_record)
            raise Exception('fail to connect to MongoDB')

    def mongodb_log(self, log_record='Unknown'):
        doc = {'time': dt.now(), 'record': log_record}
        try:
            api_record = self.mongodb['mongodb_data']
            api_record.insert_one(doc)
        except Exception:
            raise Exception

    def save_label(self, username, label, url):
        doc = {
            'twitter_id': username,
            'labels': label,
            'img_url': url,
        }
        try:
            img_info = self.mongodb['mongodb_label']
            img_info.insert_one(doc)
        except Exception:
            log_record = 'fail to save label to MongoDB. Error: {}'.format(str(Exception))
            MongoDB.mongodb_log(log_record)
            raise Exception

    def mongodb_search(self, key):
        result = []
        try:
            img_info = self.mongodb['mongodb_label']
            for col in img_info.find():
                if key in col['labels']:
                    if col['twitter_id'] in result:
                        continue
                    else:
                        result.append(col['twitter_id'])
            return result
        except Exception:
            log_record = 'fail to search keyword in MongoDB Database. Error: {}'.format(str(Exception))
            MongoDB.mongodb_log(log_record)
            raise Exception
        finally:
            self.mongodb_log('Search {} in mongodb.'.format(key))

    def mongodb_statistics(self):
        try:
            api_log = self.mongodb['mongodb_data']
            count = 0
            for i in api_log.find():
                count = count + 1
            return count
        except Exception:
            log_record = 'fail to get overall logs in MongoDB Database. Error: {}'.format(str(Exception))
            MongoDB.mongodb_log(log_record)
            raise Exception
        finally:
            self.mongodb_log('Count logs in MongoDB.')

