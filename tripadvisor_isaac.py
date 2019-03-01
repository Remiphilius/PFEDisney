# Importer des modules pour l'exploration Web
from typing import List
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import requests
import urllib

def check_internet(self):
    try:
        header = {"pragma" : "no-cache"}
        req = urllib.Request("http://www.google.ro", headers=header)
        response = urllib.urlopen(req,timeout=2)
        return True
    except urllib.URLError as err:
        return False

#fonction pour supprimer les tags HTML
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


reviews_id_List = []
reviewsList = []
notes = []

#extraire les critiques
import urllib
import time

def get_HTML(url):
    while True:
        try:
            response = urlopen(url)
            break
        except :
            time.sleep(20)
    return response

for f in range(2850,5700,10):
    url = "https://www.tripadvisor.fr/Attraction_Review-g226865-d189258-Reviews-or"+str(f)+"-Disneyland_Paris-Marne_la_Vallee_Seine_et_Marne_Ile_de_France.html"

# extraire les ids des critiques
    web = get_HTML(url).read()  # ouvrir l'URL
    source = BeautifulSoup(web,  "html.parser")  # extraire le code HTML de l'URL
    pars_ids_avis = source.findAll('div', {'class': 'review-container'})  # extraire tous les paragraphes ou y'a les ids des critiques

    # acceder aux ids des commentaires de la page i
    for avis in pars_ids_avis:
        text = list(avis.attrs.items())[1][1]
        # ajouter l'ID a la liste reviews_id_List
        print(text)
        reviews_id_List.append(text)

import os
try:
    #os.remove("/home/loic/Bureau/PFE_Disney_Git/PFEDisney/bases_de_donnees/sens_critique/crtitics_tripadvisor_ids_list.txt")
    open('/home/isaac/Documents/crtitics_tripadvisor_ids_list_isaac.txt', 'w+', encoding='utf-8', newline='')
except OSError:
    open('/home/isaac/Documents/crtitics_tripadvisor_ids_list_isaac.txt', 'w+', encoding='utf-8')
    pass

# ouvrir le fichier csv dans lequel on stockera les ids
with open('/home/isaac/Documents/crtitics_tripadvisor_ids_list_isaac.txt', 'a+', encoding='utf-8', newline='') as f:
    for i in range(len(reviews_id_List)):
        f.write(reviews_id_List[i]+"\n")
    f.close()


reviews_id_List = []
with open("/home/isaac/Documents/crtitics_tripadvisor_ids_list_isaac.txt") as file:
    for line in file:
        reviews_id_List.append(line.replace("\n",""))

try:
    #os.remove("/home/loic/Bureau/PFE_Disney_Git/PFEDisney/bases_de_donnees/sens_critique/crtitics_tripadvisor.csv")
    open('/home/isaac/Documents/crtitics_tripadvisor_isaac.csv', 'w', encoding='utf-8', newline='')
except OSError:
    open('/home/isaac/Documents/crtitics_tripadvisor_isaac.csv', 'w', encoding='utf-8', newline='')
    pass

i = 0
while i < len(reviews_id_List):
    print("dernier id: " + str(i))
    url = "https://www.tripadvisor.fr/ShowUserReviews-g226865-d189258-r"+str(reviews_id_List[i])+"-Disneyland_Paris-Marne_la_Vallee_Seine_et_Marne_Ile_de_France.html"  # Ajoutez l'URL de base des commentaires
    web = get_HTML(url)
    soup = BeautifulSoup(web.read(), "html.parser")

    a = soup.findAll('div', {'class': 'review-container'})#, "data-reviewid": str(reviews_id_List[i])})
    avis = a[0].find('p', class_='partial_entry').text.replace("\n", " ")
    rating = a[0].find('span', class_='ui_bubble_rating')
    note = list(rating.attrs.items())[0][1][1][7:9]
    print(avis)
    print(note)

    init = avis.split(sep=".")
    res = ''
    add = False
    for line in init:
        if len(line) + len(res) >= 300:
            add = True
            res = res + '. ' + line
            reviewsList.append(res)
            if (int(note) < 30):
                notes.append(-1)
            elif (int(note) == 30):
                notes.append(0)
            else:
                notes.append(1)
            res = ''
        elif (len(line) + len(res) < 300) and (len(line) > 50):
            add = True
            while len(res) < 300:
                if (res == '' or res == ' ') and line !='.':
                    res = line
                    res = res + '. ' + line
                else:
                    res = res + '. ' + line
            reviewsList.append(res)
            if (int(note) < 30):
                notes.append(-1)
            elif (int(note) == 30):
                notes.append(0)
            else:
                notes.append(1)
            res = ''
            res = ''
    if add == True:
        with open('/home/isaac/Documents/crtitics_tripadvisor_isaac.csv', 'a+', encoding='utf-8', newline='') as file:
            file.write(str(reviewsList[i]) + " µ " + str(notes[i]) + "\n")
            file.close()  # fermer le fichier
    i = i+1




# Importer le module nltk pour l'analyse de texteimport nltk
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')
import re
import unidecode
from string import punctuation
from nltk.tokenize import RegexpTokenizer

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

try:
    os.remove("/home/isaac/Documents/crtitics_tripadvisor_treated_isaac.csv")
    open('/home/isaac/Documents/crtitics_tripadvisor_treated_isaac.csv', 'w', encoding='utf-8', newline='')
except OSError:
    open('/home/isaac/Documents/crtitics_tripadvisor_treated_isaac.csv', 'w', encoding='utf-8', newline='')
    pass

reviewProcessedList = []
i = 0
# prétraiter chaque ligne par une instruction for
for line in reviewsList:
    reviewProcessed = ''
    line = remove_emoji(line)
    line = line.replace("\n", " ")
    tokens = tokenizer.tokenize(line)
    for token in tokens:
        if token.lower() not in stopWords:
            # ca depend de la methode
            # token = stemmer.stem(token)
            token = unidecode.unidecode(token)
            reviewProcessed += ' ' + token
    reviewProcessedList.append(reviewProcessed)
    with open('/home/isaac/Documents/crtitics_tripadvisor_treated_isaac.csv', 'a+', encoding='utf-8', newline='') as file:
        file.write(str(reviewProcessedList[i]) + " µ " + str(notes[i]) + "\n")
        file.close()  # fermer le fichier
    i = i + 1