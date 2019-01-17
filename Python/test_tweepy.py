import tweepy
from datetime import datetime
startTime = datetime.now()

auth = tweepy.OAuthHandler('FEblETXlgkePuX8wPzxBAjZGb', 'X4ujxbhgJ4abbgiOvaxR7QB840C8Pm4bcWB9qhQY71ifXYj1FL')
auth.set_access_token("127976412-r3ADD5H0lS0xBFuTT6qr9iDmaYgFOmlut1zwoNdw",
                      "FBJZk5J9djcpDYfIF7wjT1zSfaPJGLht5YOrqwQECQp4t")

api = tweepy.API(auth)

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    message = tweet.text.split(' ')
#    print(' '.join([word for word in message if not word[:8] == "https://"]))

tweets_research = tweepy.Cursor(api.search, q="disneyland paris").pages()

print(tweets_research.count())

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

print(datetime.now() - startTime)
