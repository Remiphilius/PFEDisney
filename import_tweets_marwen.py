import re
import csv
import tweepy
import pandas as pd
import numpy as np
from IPython.display import display
from datetime import datetime
startTime = datetime.now()

# Function to extract tweets
def get_tweets(query, max_tweets):
    _max_queries = 1000  # arbitrarily chosen value
    auth = tweepy.OAuthHandler('lddW5cut4polesn9vmcjYiASi', 'RTSgn1qwwQii2ZOIZqrwtEyUu5qads6C5d0qXK4qVBAYX0nw1M')
    auth.set_access_token("1082883910978191360-gQO0MD6wtOIasaZpDdGLKc6dUEwLyf", "pBJ26U2xhtFqMs9KhSwYUAapH3KQfOr7CcsMfIOvNIdpC")

    # Calling api
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweets = tweet_batch = api.search(q=query,
                        # geocode='1.3552217,103.8231561,100km',
                        lang='fr',
                        count=max_tweets,
                        tweet_mode = "extended")

    oldest = tweets[-1].id - 1
    print(oldest)
    ct = 1
    while len(tweets) < max_tweets and ct < _max_queries:
        print(len(tweets))
        tweet_batch = api.search(q=query,
                                 lang='fr',
                                 count=max_tweets - len(tweets),
                                 tweet_mode = "extended",
                                 max_id=oldest)
        tweets.extend(tweet_batch)
        oldest = tweets[-1].id - 1
        print(oldest)
        ct += 1
        print(tweets.max_id)

        pd.set_option('display.max_colwidth', -1)
        # We create a pandas dataframe as follows:
        data = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['Tweets'])
        # We add relevant data:
        data['len'] = np.array([len(tweet.full_text) for tweet in tweets])
        data['ID'] = np.array([tweet.id for tweet in tweets])
        data['Date'] = np.array([tweet.created_at for tweet in tweets])
        data['Source'] = np.array([tweet.source for tweet in tweets])
        data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
        data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
        display(data)

        header = [re.sub(' +', ' ', i.replace('\n', ' ')) for i in data.columns]

        with open('tweepy_results.csv', 'w') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow(header)
            for row in data.iterrows():
                writer.writerow([i for i in list(row)])

        data = pd.DataFrame(data, columns=header)
        data.to_csv('tweepy_results.csv')

get_tweets(['Disneyland','marvel'], 10000)
