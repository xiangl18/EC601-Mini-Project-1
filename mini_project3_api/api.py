import os
import io
import tweepy
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account
import urllib.request
import subprocess
import wget
import mysql
import mongodb
from collections import OrderedDict
from PIL import Image

mysql_api = mysql.MySQL()
mongodb_api = mongodb.MongoDB()


class DatabaseAPI(object):

    def __init__(self):
        self.consumer_key = ''
        self.consumer_secret = ''
        self.access_token = ''
        self.access_token_secret = ''
        self.username = 'JerrySeinfeld'
        self.output = {}
        self.url_list = []
        self.name_list = []
        self.framerate = 1
        self.json_file = ''
        self.error = None
        self.id = 0
        self.width = 900
        self.height = 600
        while True:
            self.path = input('Please input path(Please add "/" at the end of your path):')
            # Provide a default
            if not self.path:
                self.path = os.getcwd()
            # # Check whether the file is writable
            if not os.access(self.path, os.W_OK):
                print("Path not writable, please try again")
            else:
                print('use path {} as base path'.format(self.path))
                break

    def get_keys(self, consumer_key, consumer_secret, access_token, access_token_secret, json_file):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        path = (self.path, json_file)
        self.json_file = '/'.join(path)

    def twitter_images(self, count):
        try:
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            api = tweepy.API(auth)
            self.username = input('Please input a username：')
            public_tweets = api.user_timeline(screen_name=self.username, count=count, include_rts=False, exclude_replies=True)
        except tweepy.error.TweepError:
            raise Warning('fail to access the twitter by using key')
        try:
            media_files = set()
            output = OrderedDict()
            for status in public_tweets:
                if len(status.entities.get('media', [])) > 0:
                    media = status.entities.get('media', [])
                    url = status.entities['media'][0]['media_url']
                    self.url_list.append(url)
                    file_name = '{name}_{id}.jpg'.format(name=self.username, id=str(self.id).zfill(5))
                    self.name_list.append(file_name)
                    urllib.request.urlretrieve(url, file_name)
                    self.id = self.id + 1
                    output = dict(zip(self.name_list, self.url_list))
                    if (len(media) > 0):
                        media_files.add(media[0]['media_url'])
            keys = sorted(output.keys())
            self.output = OrderedDict()
            for key in keys:
                self.output[key] = output[key]
        except tweepy.error.TweepError:
            log_record = 'Error: {}'.format(str(tweepy.error.TweepError))
            mysql_api.mysql_log(log_record)
            mongodb_api.mongodb_log(log_record)
            print('error')
        finally:
            log_record = 'download {count} images from @{name}'.format(count=count, name=self.username)
            mysql_api.mysql_log(log_record)
            mongodb_api.mongodb_log(log_record)

    # get images by searching from a user's timeline.
    def search_images(self):
        try:
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            api = tweepy.API(auth)
        except tweepy.error.TweepError:
            log_record = 'Error: {}'.format(str(tweepy.error.TweepError))
            mysql_api.mysql_log(log_record)
            mongodb_api.mongodb_log(log_record)
            raise Warning('fail to access the twitter by using key')

        keyword = input('Please input a searching keyword：')
        users = api.search_users(keyword, per_page=5, page=1)
        user_list = []
        for user in users:
            user_list.append(user.name)
        if len(user_list) == 0:
            log_record = 'Warning: No result found'
            mysql_api.mysql_log(log_record)
            mongodb_api.mongodb_log(log_record)
            raise Warning("No result found")

        for name in user_list:
            try:
                public_tweets = api.user_timeline(screen_name=name, count=50)
            except Exception:
                print("No timeline for this user")
                continue
            try:
                media_files = set()
                for status in public_tweets:
                    media = status.entities.get('media', [])
                    if (len(media) > 0):
                        media_files.add(media[0]['media_url'])
                for media_file in media_files:
                    wget.download(media_file, out=self.path)
            except tweepy.error.TweepError:
                log_record = 'Error: {}'.format(str(tweepy.error.TweepError))
                mysql_api.mysql_log(log_record)
                mongodb_api.mongodb_log(log_record)
                print('error')
            finally:
                find = len(media_files)
                log_record = '{} images are found and downloaded'.format(find)
                mysql_api.mysql_log(log_record)
                mongodb_api.mongodb_log(log_record)

    def label(self):
        # Please add you json into the folder with all other code files.
        # edit and add your own json file here, replace the "\My First Project-bbdc176f5fe1.json".
        list_len = len(self.output)
        try:
            filename = self.path + "\My First Project-78c9371a06a3.json"
            credentials = service_account.Credentials.from_service_account_file(filename)
            client = vision.ImageAnnotatorClient(credentials=credentials)
        except:
            log_record = 'fail to add the json file'
            mysql_api.mysql_log(log_record)
            mongodb_api.mongodb_log(log_record)
            raise Warning("fail to add the json file")
        try:
            n = 0
            T = 0
            timeline = ['00', '00', '00']
            second = '0'
            srtfile = open('output.srt', 'w')
            frame_rate = float(self.framerate)
            for file, url in self.output.items():
                label_list = []
                with io.open(file, 'rb') as image_file:
                    content = image_file.read()
                image = types.Image(content=content)
                response = client.label_detection(image=image)
                labels = response.label_annotations

                for label in labels:
                    label_list.append(label.description)
                    mysql_api.save_label(self.username, label.description, url)
                    mongodb_api.save_label(self.username, label.description, url)

                # make srt ----
                for i in range(len(label_list)):
                    Labels = ', '.join(label_list)
                start = ':'.join(timeline) + '.' + second
                T = T + 1. / frame_rate
                timeline[2], second = str(T).split('.')
                if int(timeline[2]) == 60:
                    timeline[1] = str(int(timeline[1]) + 1)
                    timeline[2] = '00'
                    T = T - 60
                end = ':'.join(timeline) + '.' + second
                line = [str(n + 1), start + ' --> ' + end, Labels]
                line = '\n'.join(line)
                srtfile.write(line + '\n' + '\n')
                n = n + 1
        except Exception:
            self.error = Exception
            log_record = 'fail to create srt. Error: {}'.format(str(self.error))
            mysql_api.mysql_log(log_record)
            mongodb_api.mongodb_log(log_record)
            raise Exception
        finally:
            log_record = '{} images are labeled'.format(list_len)
            mysql_api.mysql_log(log_record)
            mongodb_api.mongodb_log(log_record)

    def process_video(self):
        # -y for output file overwrite
        # -r for frame rate
        # -i for input files
        # -vf for adding subtitles for output video
        try:
            cmd1 = 'ffmpeg -y -r ' + str(
                self.framerate) + ' -i ' + self.path + '/{img}_'.format(
                img=self.username) + '%01d.jpg' + ' -vf scale=900:600 ' + self.path + '/OutputVideo.mkv'
            subprocess.call(cmd1, shell=True)
            cmd2 = 'ffmpeg -y -r ' + str(
                self.framerate) + ' -i ' + self.path + '/OutputVideo.mkv' + ' -vf subtitles=output.srt ' + self.path + '/OutputVideo_label.mkv'
            subprocess.call(cmd2, shell=True)
            log_record = "video is created"
            mysql_api.mysql_log(log_record)
            mongodb_api.mongodb_log(log_record)
        except Exception:
            self.error = Exception
            log_record = 'fail to create video. Error:{}'.format(str(self.error))
            mysql_api.mysql_log(log_record)
            mongodb_api.mongodb_log(log_record)
            raise Exception

    def search(self, key):
        users_mysql = mysql_api.mysql_search(key)
        print('In MySQL Database, The users with keyword {} are as follows:'.format(key))
        for user in users_mysql:
            print(user)
        users_mongodb = mongodb_api.mongodb_search(key)
        print('In MongoDB Database, The users with keyword {} are as follows:'.format(key))
        for user in users_mongodb:
            print(user)

        # resize images
    def image_process(self):
        for file in self.name_list:
            im = Image.open(file)
            out = im.resize((self.width, self.height), Image.ANTIALIAS)
            out.save(file)

    def statistics(self):
        mysql_record, mysql_collection = mysql_api.mysql_statistics()
        mongodb_record, mongodb_collection = mongodb_api.mongodb_statistics()
        print(mysql_record[0], 'logs in MySQL Database.\n')
        print('The 3 most  popular labels in MySQL Database are:\n'
              '{c1} for {c1x} times\n'
              '{c2} for {c2x} times\n'
              '{c3} for {c3x} times\n'.format(c1=mysql_collection[0][0], c1x=mysql_collection[0][1],
                                              c2=mysql_collection[1][0], c2x=mysql_collection[1][1],
                                              c3=mysql_collection[2][0], c3x=mysql_collection[2][1]))
        print(mongodb_record, 'logs in MongoDB Databse.\n')
        print('The 3 most  popular labels in MongoDB Database are:\n'
              '{c1} for {c1x} times\n'
              '{c2} for {c2x} times\n'
              '{c3} for {c3x} times\n'.format(c1=mongodb_collection[0][0], c1x=mongodb_collection[0][1],
                                              c2=mongodb_collection[1][0], c2x=mongodb_collection[1][1],
                                              c3=mongodb_collection[2][0], c3x=mongodb_collection[2][1]))

