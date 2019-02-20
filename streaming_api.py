import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time

auth = tweepy.OAuthHandler('lddW5cut4polesn9vmcjYiASi', 'RTSgn1qwwQii2ZOIZqrwtEyUu5qads6C5d0qXK4qVBAYX0nw1M')
auth.set_access_token("1082883910978191360-gQO0MD6wtOIasaZpDdGLKc6dUEwLyf", "pBJ26U2xhtFqMs9KhSwYUAapH3KQfOr7CcsMfIOvNIdpC")
api = tweepy.API(auth)

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):

        all_data = json.loads(data)

        if all_data['truncated'] == True:
            tweet = all_data["extended_tweet"]["full_text"]
            print("**************************")
        else:
            tweet = all_data["text"]

        #tweet = all_data["extended_tweet"]["full_text"]
        username = all_data["user"]["screen_name"]
        language = all_data["lang"]
        id = all_data["id"]
        date = all_data["created_at"]


        with open('bases_de_donnees/tweets_streaming.txt', 'a', encoding='utf-8') as f:
            f.write(username+', '+tweet.replace("\n", " ")+', '+language+', '+str(id)+', '+date+'\n')
            f.close()
        

        print((username, tweet, language, id))

        return True

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            # returning False in on_data disconnects the stream
            '''
            time.sleep(7200)

            tweets_research = tweepy.Cursor(api.search, q="disneyland paris",lang='fr',)

            for tweet in limit_handled(tweets_research.items()):
                with open('bases_de_donnees/tweets_streaming.txt', 'a', encoding='utf-8') as f:
                    f.write(tweet.id + ', ' + tweet.full_text.replace("\n", " ") + '\n')
                    f.close()
            return True

        else:'''
            return False

l = StdOutListener()
myStream = Stream(auth, l)
myStream.filter(track=['paris disneyland', 'disneylandparis'], is_async=True)

