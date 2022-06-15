# %%

import json
import re
import spacy

import pandas
#pandas._version_

import matplotlib.pyplot as plt
import numpy as np

# adds scripts/ and src/ folder: so you can import scripts/functions across project steps
import sys 
sys.path.append("../../src")
sys.path.append("../../scripts")



# %%
def from_texts_to_listByType(listOfTexts):
    """
    Trie les textes de propriétaires en fonction de leur catégories
    
    paramètre :
        listOfTexts (liste de tuples (int, string)): la liste des entrées et leur nombre d'occurrences
    
    retourne :
        result (liste de tuplet (string, liste de tuples (int, string)):
                Les entrées classées en plusieurs listes, une par catégories. Chaque liste porte le nom de la catégorie associé

    """
    length = len(listOfTexts)

    other = []
    venezia = []
    demanio = []
    chiesa = []
    congregazione = []
    nameSolo = []
    nameEFratello = []
    nameQuondam = []
    nameSic = []
    irrelevant = []
    
    for i in range(length):
        word = listOfTexts[i][1]
        if re.search("(citt..|comm?une) di venezia", word, re.IGNORECASE) is not None:
            venezia.append(listOfTexts[i])
        elif re.search("(regio )?deman(i|e)o|ministe?ro|reale corona|tesoro|^ufficio del censo", word, re.IGNORECASE) is not None:
            demanio.append(listOfTexts[i])
        elif re.search("chiesa|monastero|benefi(c|z)io|^capitolo|^prebenda", word, re.IGNORECASE): #capitolo,prebende, beneficio
            chiesa.append(listOfTexts[i])
        elif re.search("congregazione", word, re.IGNORECASE):
            congregazione.append(listOfTexts[i])
        elif re.search("^(eredi del fu )?([a-z]|'|Ã²|ò)+ ?(([a-z]|Ã²|ò)+ )?(di )?([a-z]|Ã²|ò)+ *$", word, re.IGNORECASE):
            nameSolo.append(listOfTexts[i])
        elif re.search("^([a-z]|'|Ã²|ò)+( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²|ò)+)?( (q\.m?\.?|quondam|vedova( di)?)( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²|ò)+)?( (\.)+)?)+$",word,re.IGNORECASE):
            nameQuondam.append(listOfTexts[i])
        elif re.search("^([a-z]|'|Ã²|ò)+( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²ò)+)?( ed? ([a-z]|'|Ã²ò)+)?(( e)? (fratell(i|o)|sorelle))?(( (q\.m?\.?)| (quondam)| (vedova( di)?)) ([a-z]|'|Ã²ò)+( di)?( ([a-z]|'|Ã²ò)+)?)*( indivisi)?$", word, re.IGNORECASE):
            nameEFratello.append(listOfTexts[i])     #e avec un point d'interrogation
        elif re.search("sic|\.{4,15}", word, re.IGNORECASE):
            nameSic.append(listOfTexts[i])
        elif re.search("^(|-|N\.)$|^possessore ignoto", word, re.IGNORECASE):
            irrelevant.append(listOfTexts[i])
        else:
            other.append(listOfTexts[i])
 
        result = [("Venezia", venezia),("Demanio",demanio),("Chiesa",chiesa),("Congregazione",congregazione),
            ("NomSeul", nameSolo),("NomEtQuondam",nameQuondam),("NomAvecFamille",nameEFratello),
            ("Sic",nameSic),("Irrelevant",irrelevant),("Other",other)] 

    return result
    
def from_textsPlusParcels_to_listBytype(ListofTextsPlusParcels):
    """
    Trie les textes de propriétaires en fonction de leur catégories
    
    paramètre :
        listOfTextsPlusParcels ( [list de String, liste de liste d'integer] ): 
                la liste des entrées, chacune associée aux parcelles qu'elle possède (se situe au même index dans les deux listes principales) 
    
    retourne :
        result (liste de tuplet (string, liste de tuples (int, string)):
                Les entrées classées en plusieurs listes, une par catégories. Chaque liste porte le nom de la catégorie associé

    """ 
       
    length = len(ListofTextsPlusParcels[0])

    other = []
    venezia = []
    demanio = []
    chiesa = []
    congregazione = []
    nameSolo = []
    nameEFratello = []
    nameQuondam = []
    nameSic = []
    irrelevant = []
    
    for i in range(length):
        Word = ListofTextsPlusParcels[0][i]
        if re.search("(citt..|comm?une) di venezia", Word, re.IGNORECASE) is not None:
            venezia.append((ListofTextsPlusParcels[0][i],ListofTextsPlusParcels[1][i]))
        elif re.search("(regio )?deman(i|e)o|ministe?ro|reale corona|tesoro|^ufficio del censo", Word, re.IGNORECASE) is not None:
            demanio.append((ListofTextsPlusParcels[0][i],ListofTextsPlusParcels[1][i]))
        elif re.search("chiesa|monastero|benefi(c|z)io|^capitolo|^prebenda", Word, re.IGNORECASE): #capitolo,prebende, beneficio
            chiesa.append((ListofTextsPlusParcels[0][i],ListofTextsPlusParcels[1][i]))
        elif re.search("congregazione", Word, re.IGNORECASE):
            congregazione.append((ListofTextsPlusParcels[0][i],ListofTextsPlusParcels[1][i]))
        elif re.search("^(eredi del fu )?([a-z]|'|Ã²|ò)+ ?(([a-z]|'|Ã²|ò)+ )?(di )?([a-z]|'|Ã²|ò)+ *$", Word, re.IGNORECASE):
            nameSolo.append((ListofTextsPlusParcels[0][i],ListofTextsPlusParcels[1][i]))
        elif re.search("^([a-z]|'|Ã²|ò)+( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²|ò)+)?( (q\.m?\.?|quondam|vedova( di)?)( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²|ò)+)?( (\.)+)?)+$",Word,re.IGNORECASE):
            nameQuondam.append((ListofTextsPlusParcels[0][i],ListofTextsPlusParcels[1][i]))
        elif re.search("^([a-z]|'|Ã²|ò)+( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²ò)+)?( ed? ([a-z]|'|Ã²ò)+)?(( e)? (fratell(i|o)|sorelle))?(( (q\.m?\.?)| (quondam)| (vedova( di)?)) ([a-z]|'|Ã²ò)+( di)?( ([a-z]|'|Ã²ò)+)?)*( indivisi)?$", Word, re.IGNORECASE):
            nameEFratello.append((ListofTextsPlusParcels[0][i],ListofTextsPlusParcels[1][i]))     #e avec un point d'interrogation
        elif re.search("sic|\.{4,15}", Word, re.IGNORECASE):
            nameSic.append((ListofTextsPlusParcels[0][i],ListofTextsPlusParcels[1][i]))
        elif re.search("^(|-|N\.)$|^possessore ignoto", Word, re.IGNORECASE):
            irrelevant.append((ListofTextsPlusParcels[0][i],ListofTextsPlusParcels[1][i]))
        else:
            other.append((ListofTextsPlusParcels[0][i],ListofTextsPlusParcels[1][i]))

        result = [("Venezia", venezia),("Demanio",demanio),("Chiesa",chiesa),("Congregazione",congregazione),
            ("NomSeul", nameSolo),("NomEtQuondam",nameQuondam),("NomAvecFamille",nameEFratello),
            ("Sic",nameSic),("Irrelevant",irrelevant),("Other",other)]       
    
    return result 

#%%
def from_listByType_to_barChart(listByType):
    """
    Construit un diagramme à barres du nombre d'entrée par catégories et du nombre de parcelles possédées par chacune des catégories.
    Affiche ce diagramme ainsi que les nombres utlisés pour le construire.

    paramètre : 
        listByType (liste de tuplet (string, liste de tuples (int, string)):
                Les entrées classées en plusieurs listes, une par catégories. Chaque liste porte le nom de la catégorie associé
    
    ne retourne rien
    
    """

    nb_entrees = []
    nb_parcelles = []
    nb_cat = 0

    for [nom, liste] in listByType:
        nb_entrees.append(len(liste))
        sum = 0
        for [x, y] in liste:
            sum += x
        nb_parcelles.append(sum)
        nb_cat += 1
        print(nom, " : entrées = ",len(liste)," parcelles = ", sum)

    #fig, ax = plt.subplots()
    index = np.arange(nb_cat)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, nb_entrees, bar_width,
    alpha=opacity,
    color='b',
    label='nombre d\'entrées  avec des noms différents')

    rects2 = plt.bar(index + bar_width, nb_parcelles, bar_width,
    alpha=opacity,
    color='g',
    label='nombre de parcelles')

    plt.xlabel('type de propriétaire')
    plt.ylabel('nombre')
    plt.title('répartition des propriétaires par type')
    plt.xticks(index + bar_width, ('venezia', 'demanio', 'chiesa', 'congreg.','nom seul', 'quondam',
        'famille','sic','irrelevant','autres' ), rotation=40)
    plt.legend()

    plt.tight_layout()
    plt.show()

