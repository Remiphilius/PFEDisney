import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time

auth = tweepy.OAuthHandler('lddW5cut4polesn9vmcjYiASi', 'RTSgn1qwwQii2ZOIZqrwtEyUu5qads6C5d0qXK4qVBAYX0nw1M')
auth.set_access_token("1082883910978191360-gQO0MD6wtOIasaZpDdGLKc6dUEwLyf", "pBJ26U2xhtFqMs9KhSwYUAapH3KQfOr7CcsMfIOvNIdpC")
api = tweepy.API(auth, wait_on_rate_limit=True)

tweet = api.get_status(id=1097457259943063554)
print(tweet)