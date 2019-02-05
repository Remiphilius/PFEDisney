# Importer des modules pour l'exploration Web
from typing import List
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

#fonction pour supprimer les tags HTML
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

#faire une liste des films marvel avec leurs IDs
film = ['Avengers','Les_Gardiens_de_la_galaxie','Iron_Man','X_Men_Le_Commencement','Spider_Man','X_Men_Days_of_Future_Past','Logan','Avengers_Infinity_War','Spider_Man_2','Captain_America_Le_Soldat_de_l_hiver',
        'X_Men','Captain_America_Civil_War','X_Men_2','Deadpool','Avengers_L_Ere_d_Ultron','Les_Gardiens_de_la_galaxie_Vol_2','Doctor_Strange']
id_film = ['493660','406937','451223','487010','387292','422063','11082226','9008787','434094','395521','446853','11040752','468827','362143','437798','11867538','392811']
type ='filter-negative' #type des reviews
reviewsList = []
page_no = 10  # nombre de pages à parcourir par film
f=0

for f in range(len(film)):
    reviews_id_List = []
    status = True
    i = 1

    # extraire les ids des critiques des 10 premieres pages avec une boucle
    while status:
        url = 'https://www.senscritique.com/film/'+film[f]+'/'+id_film[f]+'/critiques#page-'+str(i)+'/'+type+'/'  # Ajoutez l'URL de départ
        web = urlopen(url)  # ouvrir l'URL
        source = BeautifulSoup(web, 'html.parser')  # Bextraire le code HTML de l'URL
        pars = source.findAll('button', {'class': 'ere-review-overview'})  # extraire tous les paragraphes ou y'a les ids des critiques

        # acceder aux ids des commentaires de la page i
        for par in pars:
            text = str(par.get_text).replace('<bound method Tag.get_text of <button class="ere-review-overview" data-rel="review-overview" data-sc-review-id="', '').replace('" type="button"><span class="eins-sprite eins-zoom "></span></button>>', '')
            # ajouter l'ID a la liste reviews_id_List
            reviews_id_List.append(text)
        i += 1  # incrementer le compteur
        if i >= page_no:  # ne pas depasser les 10 premieres pages
            status = False

    #extraire les critiques
    i = 0
    while i < len(reviews_id_List):
        url = 'https://www.senscritique.com/film/'+film[f]+'/critique/'+str(reviews_id_List[i])  # Ajoutez l'URL de base des commentaires
        web = urlopen(url)  # ouvrir l'URL
        source = BeautifulSoup(web, 'html.parser')  # extraire le code HTML de l'URL
        pars = source.findAll('div', {'class': 'rvi-review-content'})  # extraire le paragraphe ou se trouve la critique

        # nettoyer le resultat et l'ajouter à la liste des critiques
        for par in pars:
            text = cleanhtml(str(par.get_text)).replace('\n',' ').replace('>', ' ')
            reviewsList.append(text)
            print(text)
        i += 1

    f += 1

# ouvrir le fichier csv dans lequel on stockera les critiques positives
with open(type+'crtitics.txt', 'w', encoding='utf-8') as f:
    for review in reviewsList:  # loop sur les differents avis positifs
        f.write(review + '\n')
    f.close()  # fermer le fichier
