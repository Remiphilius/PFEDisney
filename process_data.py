# Importer le module nltk pour l'analyse de texteimport nltk
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
import re
import unidecode
from string import punctuation
from nltk.tokenize import RegexpTokenizer


def process_sens_critique_data(file, sortie):
    # Algo de stemming permettant de supprimer automatiquement les suffixes pour n'obtenir que la racine des mots. On parle de racinisation.
    stemmer = nltk.stem.SnowballStemmer('french')

    # Invoquer des mots vides en francais et les stocker dans des variables
    stopWords = stopwords.words('french')

    tokenizer = RegexpTokenizer(r'\w+')

    def remove_emoji(string):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

    # Ouvrir le fichier 'result-1-3-5-inception.txt' avec la fonction open et l'attribuer à f
    with open(file, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        f.close()

    reviewProcessedList = []

    # prétraiter chaque ligne par une instruction for
    for line in lines:
        reviewProcessed = ''
        line = remove_emoji(line)
        tokens = tokenizer.tokenize(line)
        for token in tokens:
            if token.lower() not in stopWords:
                token = stemmer.stem(token)
                token = unidecode.unidecode(token)
                reviewProcessed += ' ' + token
        reviewProcessedList.append(reviewProcessed)

    # Ouvrir le fichier 'result-2-2-4-inception.txt' avec la fonction open et l'attribuer à f
    with open(sortie, 'w', encoding = 'utf-8') as f:
        for reviewProcessed in reviewProcessedList:
            f.write(reviewProcessed + '\n')
        f.close()

process_sens_critique_data("/home/ensai/PycharmProjects/PFEDisney/bases_de_donnees/sens_critique/filter-negativecrtitics.txt","/home/ensai/PycharmProjects/PFEDisney/bases_de_donnees/sens_critique/negative_crtitics_processesed.txt")