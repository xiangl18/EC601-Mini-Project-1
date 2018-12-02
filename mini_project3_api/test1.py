import api

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
json_file = ''

api = api.DatabaseAPI()
api.get_keys(consumer_key, consumer_secret, access_token, access_token_secret, json_file)
api.twitter_images(200)
api.label()
api.process_video()
api.search('car')
api.statistics()

