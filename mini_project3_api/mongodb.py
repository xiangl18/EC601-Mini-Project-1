import pymongo
from datetime import datetime as dt

class MongoDB(object):
    def __init__(self):
        self.error = None
        try:
            mongodb = pymongo.MongoClient('mongodb://localhost')
            self.mongodb = mongodb['twitter_database']
        except Exception:
            raise Exception('fail to connect to MongoDB')

    def mongo_log(self, log_record='Unknown'):
        if self.error:
            log_record = str(self.error)
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
            self.error = Exception
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
        except Exception as e:
            self.error = e
            raise e
        finally:
            self.mongo_log('Search {} in mongodb.'.format(key))

    def mongo_statistics(self):
        try:
            api_log = self.mongodb['mongodb_data']
            count = 0
            for i in api_log.find():
                count = count + 1
            return count
        except Exception as e:
            self.error = e
            raise e
        finally:
            self.mongo_log('Count logs in MongoDB.')

