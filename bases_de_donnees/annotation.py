import pandas  as pd

def annotation(first_line=0, file="tweets_streaming.txt"):
    df = pd.read_csv("tweets_streaming.csv", error_bad_lines=False, sep=";")
    with open(file, 'r') as fichier_txt:
