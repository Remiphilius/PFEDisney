import pickle as pkl
import tweepy
import collections

with open('listtweets.pkl', 'rb') as f:  # on dirait que pickle n'a pas pu enregistrer une liste assez longue
    listtweets = pkl.load(f)

tweet1 = listtweets[0]

langues = collections.Counter()
for tweetDLPM in listtweets:
    print(tweetDLPM.lang)
    lang = tweetDLPM.lang[0]
    langues += collections.Counter(lang)

print(langues, len(listtweets))
