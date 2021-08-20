#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import webbrowser
import sys 

def get_match(url):
    """Fonction qui cherche les liens des matchs sur une page"""
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, "html5lib")

    # Cherche tous les liens sur la page
    print("Recherche des matchs ...")
    liens = soup.findAll('a', {"class":"game-name"})

    resultat = [lien["href"] for lien in liens]
    print(f"{len(resultat)} matchs trouvés !\n")
    return resultat


def get_video_links(url):
    # Create response object 
    print("\nRequête envoyée ...")
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, "html5lib")

    # Cherche tous les liens sur la page
    print("Récupération des liens ...")
    liens = soup.findAll('a')
    # Liste avec les liens 
    liste_lien = [str(lien) for lien in liens]
    vrai_liens = [ref for ref in liste_lien if "src" in ref]

    return vrai_liens 


def ouvre_lien(liste):
    num_lien = input("\nNuméro du lien:\t")

    while len(num_lien) < 1:
        num_lien = input("\nNuméro du lien:\t")

    webbrowser.open_new_tab(liste[int(num_lien)])


def get_name(nom):
    """Fonction qui trouve le nom des matchs à partir d'une url"""
    nom = nom.split("regarder")[-1]
    nom = nom.split("-streaming")[0]
    nom = nom.replace("-", " ")
    return nom.title() # title pour majuscule au debut de chaque mot


def tri_balise(liste_parent, startswith, separateur=" "):
        
    new_list = list()
    for i in range(len(liste_parent)):
        lignes = liste_parent[i].split(separateur)
        for ligne in lignes:
            if ligne.startswith(startswith):
                new_list.append(ligne)
    return new_list 
    
def search_and_print_links(url):
    liens_sport = get_video_links(url)
    print("Informations récupérées !")

    onclick_sportif = tri_balise(liens_sport, "onclick")

    print("Tri des informations ...\n")

    src_sport = [texte.split("src")[-1] for texte in onclick_sportif]

    https_sport = [texte.split(";")[0].split("'")[1] for texte in src_sport]
    https_sport = [http for http in https_sport if http.startswith("https")]
        
    # certains liens contiennent un sous-lien, on prefère prendre le lien original:
    for i, http in enumerate(https_sport):
        if "id" in http:
            https_sport[i] = http.split("id=")[-1]
        
    if len(https_sport) > 0:

        print("Possibles liens trouvés :\n")
        for i, http in enumerate(https_sport):
            print(f"{i} - {http}")

        print("\nPour poursuivre, Ctrl+Clic sur le lien, ou entrer son numéro\n")
        
        continuer = "o"
        while continuer == "o":
            ouvre_lien(https_sport)
        
            continuer = input("Continuer ? (o/n)  ")
            continuer = continuer.lower()

            if continuer == "n":
                break 
    else:
        print("Aucun lien trouvé")

def main():

    # Message de bienvenue
    print(80 * "=")
    print(18 * " ", "Bienvenue sur le StreamonSport de Luk")
    print(80 * "=" + 4 *"\n")
    print("Attention, première version de l'application.\nBien entrer les informations pour ne pas la faire planter !\n\n")
    # URL des pages 
    url_menu = "https://www.streamonsport.info/"
    url_foot = "https://www.streamonsport.info/1-streaming-football-en-direct-euro-2021.html"

    """ Dans un premier temps on cherche les liens des différents matchs étant sur le site.
        On prend leur url, trouve leur nom et les associe dans un dictionnaire.
    """

    url_matches = get_match(url_foot)
    if len(url_matches) > 0:

        noms_matches = [get_name(match) for match in url_matches]
        dico_url_nom = {nom: match for nom, match in zip(noms_matches, url_matches)}

        for i, match in enumerate(noms_matches):
            print(f"{i} - {match}")
        """Ici on demande à l'utilisateur quel match l'intéresse :"""

        num_match= input("\nEntrer numéro du match : ")

        while len(num_match) < 1:
            num_match= input("\nEntrer numéro du match : ")

        try:
            num_match = int(num_match)
            # Le numéro choisi/index de la liste donne le texte associé et permet de retrouver le lien grâce au dico
            url_sport = dico_url_nom[noms_matches[num_match]]  
            print(f"URL de la page :{url_sport} \n")

            """Une fois le lien de la page recupéré on cherche les vidéos"""
            search_and_print_links(url_sport)
            
        except Exception as e:
            print("Erreur de saisie :", e)
            sys.exit
    
    else:
        print(f"Aucun match trouvé\nVoir URL:{url_foot} puis entrer URL du match\n")
        url_match = input("URL du match : ")
        search_and_print_links(url_match)
        

if __name__ == "__main__":
    main()