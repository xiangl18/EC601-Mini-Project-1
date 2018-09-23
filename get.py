import tweepy
import wget
import os
from PIL import Image


# get images from twitter by using tweepy api.
# add your own twitter developer key.
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


# get images from a user's homeline.
def twitter_images(path):
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        public_tweets = api.home_timeline(count=100)
    except tweepy.error.TweepError:
        raise Warning('fail to access the twitter by using key')
    
    try:
        media_files = set()
        for status in public_tweets:
            media = status.entities.get('media', [])
            if (len(media) > 0):
                media_files.add(media[0]['media_url'])
        for media_file in media_files:
            wget.download(media_file, out=path)
    except tweepy.error.TweepError:
        print('error')


# get images by searching from a user's homeline.
def search_images(path):
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except tweepy.error.TweepError:
        raise Warning('fail to access the twitter by using key')
        
    keyword = input('Please input a searching keyword：')
    users = api.search_users(keyword, per_page=5, page=1)
    user_list = []
    for user in users:
        user_list.append(user.name)
    if len(user_list) == 0:
        print("No result found")

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
                wget.download(media_file, out=path)
        except tweepy.error.TweepError:
            print('error')


# resize images
def image_process(path, width, height):
    n = 0
    filelist = os.listdir(path)
    for file in filelist:
        im = Image.open(path + file)
        out = im.resize((width, height), Image.ANTIALIAS)
        out.save(path + file)
        oldname = path + file
        d = str(n + 1)
        s = d.zfill(5)
        newname = path + s + '.jpg'
        os.rename(oldname, newname)
        n = n + 1
