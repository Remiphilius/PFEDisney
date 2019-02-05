from typing import List, Any

import tweepy
import pickle as pkl
from datetime import datetime
startTime = datetime.now()

auth = tweepy.OAuthHandler('lddW5cut4polesn9vmcjYiASi', 'RTSgn1qwwQii2ZOIZqrwtEyUu5qads6C5d0qXK4qVBAYX0nw1M')
auth.set_access_token("1082883910978191360-gQO0MD6wtOIasaZpDdGLKc6dUEwLyf",
                      "pBJ26U2xhtFqMs9KhSwYUAapH3KQfOr7CcsMfIOvNIdpC")

api = tweepy.API(auth)

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    message = tweet.text.split(' ')
#    print(' '.join([word for word in message if not word[:8] == "https://"]))

tweets_research = tweepy.Cursor(api.search, q="disneyland paris").items()

list_tweets = list()
for tweetDLP in tweets_research:
    list_tweets.append(tweetDLP)

print(list_tweets.__sizeof__())

with open('listtweets.pkl', 'wb') as f:
    pkl.dump(list_tweets, f)

#for tweet in tweets_research:
#    print(tweet.author.screen_name, ":", tweet.text, twee)

#moi = api.me()

#mes_tweets = moi.timeline(count=moi.statuses_count)

#my_lt = moi.timeline(include_rts=False)[0]
#print(my_lt.place.full_name)

#donald = api.get_user("realDonaldTrump")

#interessant = tweepy.Cursor(api.user_timeline, screen_name="@realDonaldTrump", tweet_mode="extended").items()

#for tweet in interessant:
#    if "extended_entities" in tweet.__dict__.keys():
#        if tweet.favorite_count > 10000:
#            media = tweet.extended_entities['media']
#            for i in range(len(media)):
#                print(media[i]["media_url_https"], tweet.favorite_count)

#Vive le vent d'hiver

print(datetime.now() - startTime)
