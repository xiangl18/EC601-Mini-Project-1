import pymongo
from datetime import datetime as dt
from collections import Counter


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
            data = self.mongodb['mongodb_data']
            data.insert_one(doc)
        except Exception:
            raise Exception

    def save_label(self, username, label, url):
        doc = {
            'twitter_id': username,
            'labels': label,
            'img_url': url,
        }
        try:
            label = self.mongodb['mongodb_label']
            label.insert_one(doc)
        except Exception:
            log_record = 'fail to save label to MongoDB. Error: {}'.format(str(Exception))
            MongoDB.mongodb_log(log_record)
            raise Exception

    def mongodb_search(self, key):
        result = []
        try:
            label = self.mongodb['mongodb_label']
            for c in label.find():
                if key in c['labels']:
                    if c['twitter_id'] in result:
                        continue
                    else:
                        result.append(c['twitter_id'])
            return result
        except Exception:
            log_record = 'fail to search keyword in MongoDB Database. Error: {}'.format(str(Exception))
            MongoDB.mongodb_log(log_record)
            raise Exception
        finally:
            self.mongodb_log('Search {} in mongodb.'.format(key))

    def mongodb_statistics(self):
        try:
            collection1 = self.mongodb['mongodb_data']
            collection2 = self.mongodb['mongodb_label']
            count = 0
            results = collection2.find().sort('labels', pymongo.ASCENDING)
            collection = []
            for result in results:
                collection.append(result['labels'])
            for i in collection1.find():
                count = count + 1
        except Exception:
            log_record = 'fail to get overall report in MongoDB Database. Error: {}'.format(str(Exception))
            MongoDB.mongodb_log(log_record)
            raise Exception
        finally:
            self.mongodb_log('Count logs in MongoDB.')
            self.mongodb_log('Find 3 most popular labels in MongoDB.')
            return count, Counter(collection).most_common(3)
