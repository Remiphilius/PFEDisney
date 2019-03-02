import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time

auth = OAuthHandler('lddW5cut4polesn9vmcjYiASi', 'RTSgn1qwwQii2ZOIZqrwtEyUu5qads6C5d0qXK4qVBAYX0nw1M')
auth.set_access_token("1082883910978191360-gQO0MD6wtOIasaZpDdGLKc6dUEwLyf",
                      "pBJ26U2xhtFqMs9KhSwYUAapH3KQfOr7CcsMfIOvNIdpC")
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
        tweet = ""
        all_data = json.loads(data)
        if 'truncated' in all_data.keys():
            if all_data['truncated'] == True:
                tweet = all_data["extended_tweet"]["full_text"]
                print("**************************")
            else:
                tweet = all_data["text"]

        # tweet = all_data["extended_tweet"]["full_text"]
        username = all_data["user"]["screen_name"]
        language = all_data["lang"]
        id = all_data["id"]
        date = all_data["created_at"]
        source = all_data["source"]
        print(source, username, language, id)

        # Parameters of the filter
        list_sources_allowed = ["Twitter for iPhone", "Twitter for Android", "Twitter Web Client", "Twitter Web App",
                                "Twitter for iPad", "Instagram", "Facebook",
                                "Curious Cat", "Foursquare"]  # sources dont l'on accepte la provenance des tweets

        list_lang_wanted = ["fr"]  # langues que l'on souhaite garder

        list_user_denied = ["dlp", "disney", "promo", "parcmoinscher"]  # mots que l'on ne veut pas dans le nom des utilisateurs

        list_user_accepted = ['foliedisney']  # utilisateurs qui ne passent pas le filtre précédent mais
        # pour lesquels on force le passage

        if (all_data['lang'] in list_lang_wanted) and (tweet[:2] != 'RT') and any(
                [src in source for src in list_sources_allowed]):
            if (not any([user_dnd in username.lower() for user_dnd in list_user_denied])) \
                    or username.lower() in list_user_accepted:
                tweet = tweet.replace('"', '')
                tweet = tweet.replace('µ', '')
                tweet = tweet.replace('μ', '')
                if len(tweet) > 1:  # on enleve l'@ et les url
                    list_words_no_at = [word for word in tweet.split(' ') if not (('@' in word) or ('http' in word))]
                    tweet = ' '.join(list_words_no_at)
                with open('bases_de_donnees/tweet_streaming.csv', 'a', encoding='utf-8') as f:
                    f.write(username + 'µ ' + tweet.replace("\n", " ") + 'µ ' + language + 'µ' + str(id) +
                            "a" + 'µ ' + date + 'µ ' + '\n')
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
myStream.filter(track=["disneyland"],
                is_async=True)  # 'paris disneyland', 'disneylandparis', 'disneyland paris', 'eurodisney'
