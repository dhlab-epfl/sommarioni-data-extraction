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

# import data filepath we want to use
from data_filepaths import s0_raw_sommarioni
from data_filepaths import s0_list_of_terms
from data_filepaths import s0_list_of_tronques
#from data_filepaths import s0_terms_only

# %%
def from_countedTronqued_listByTypes(ListOfTronqued):
    Length = len(ListOfTronqued)

    Other = []
    Venezia = []
    Demanio = []
    Chiesa = []
    Congregazione = []
    NameSolo = []
    NameEFratello = []
    NameQuondam = []
    NameFlou = []
    Irrelevant = []
    
    for i in range(Length):
        Word = ListOfTronqued[i][1]
        if re.search("(citt..|comm?une) di venezia", Word, re.IGNORECASE) is not None:
            Venezia.append(ListOfTronqued[i])
        elif re.search("(regio )?deman(i|e)o|ministe?ro|reale corona|tesoro|^ufficio del censo", Word, re.IGNORECASE) is not None:
            Demanio.append(ListOfTronqued[i])
        elif re.search("chiesa|monastero|benefi(c|z)io|^capitolo|^prebenda", Word, re.IGNORECASE): #capitolo,prebende, beneficio
            Chiesa.append(ListOfTronqued[i])
        elif re.search("congregazione", Word, re.IGNORECASE):
            Congregazione.append(ListOfTronqued[i])
        elif re.search("^(eredi del fu )?([a-z]|'|Ã²|ò)+ ?(([a-z]|Ã²|ò)+ )?(di )?([a-z]|Ã²|ò)+ *$", Word, re.IGNORECASE):
            NameSolo.append(ListOfTronqued[i])
        elif re.search("^([a-z]|'|Ã²|ò)+( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²|ò)+)?( (q\.m?\.?|quondam|vedova( di)?)( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²|ò)+)?( (\.)+)?)+$",Word,re.IGNORECASE):
            NameQuondam.append(ListOfTronqued[i])
        elif re.search("^([a-z]|'|Ã²|ò)+( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²ò)+)?( ed? ([a-z]|'|Ã²ò)+)?(( e)? (fratell(i|o)|sorelle))?(( (q\.m?\.?)| (quondam)| (vedova( di)?)) ([a-z]|'|Ã²ò)+( di)?( ([a-z]|'|Ã²ò)+)?)*( indivisi)?$", Word, re.IGNORECASE):
            NameEFratello.append(ListOfTronqued[i])     #e avec un point d'interrogation
        elif re.search("sic|\.{4,15}", Word, re.IGNORECASE):
            NameFlou.append(ListOfTronqued[i])
        elif re.search("^(|-|N\.)$|^possessore ignoto", Word, re.IGNORECASE):
            Irrelevant.append(ListOfTronqued[i])
        else:
            Other.append(ListOfTronqued[i])

        Result = [("NomSeul", NameSolo),("NomEtQuondam",NameQuondam),("NomAvecFamille",NameEFratello)]        
    
    return Result
    
def from_countedplusnumber_to_listBytype(ListofTronquedplusnumber):
    Length = len(ListofTronquedplusnumber[0])

    Other = []
    Venezia = []
    Demanio = []
    Chiesa = []
    Congregazione = []
    NameSolo = []
    NameEFratello = []
    NameQuondam = []
    NameFlou = []
    Irrelevant = []
    
    for i in range(Length):
        Word = ListofTronquedplusnumber[0][i]
        if re.search("(citt..|comm?une) di venezia", Word, re.IGNORECASE) is not None:
            Venezia.append((ListofTronquedplusnumber[0][i],ListofTronquedplusnumber[1][i]))
        elif re.search("(regio )?deman(i|e)o|ministe?ro|reale corona|tesoro|^ufficio del censo", Word, re.IGNORECASE) is not None:
            Demanio.append((ListofTronquedplusnumber[0][i],ListofTronquedplusnumber[1][i]))
        elif re.search("chiesa|monastero|benefi(c|z)io|^capitolo|^prebenda", Word, re.IGNORECASE): #capitolo,prebende, beneficio
            Chiesa.append((ListofTronquedplusnumber[0][i],ListofTronquedplusnumber[1][i]))
        elif re.search("congregazione", Word, re.IGNORECASE):
            Congregazione.append((ListofTronquedplusnumber[0][i],ListofTronquedplusnumber[1][i]))
        elif re.search("^(eredi del fu )?([a-z]|'|Ã²|ò)+ ?(([a-z]|'|Ã²|ò)+ )?(di )?([a-z]|'|Ã²|ò)+ *$", Word, re.IGNORECASE):
            NameSolo.append((ListofTronquedplusnumber[0][i],ListofTronquedplusnumber[1][i]))
        elif re.search("^([a-z]|'|Ã²|ò)+( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²|ò)+)?( (q\.m?\.?|quondam|vedova( di)?)( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²|ò)+)?( (\.)+)?)+$",Word,re.IGNORECASE):
            NameQuondam.append((ListofTronquedplusnumber[0][i],ListofTronquedplusnumber[1][i]))
        elif re.search("^([a-z]|'|Ã²|ò)+( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²ò)+)?( ed? ([a-z]|'|Ã²ò)+)?(( e)? (fratell(i|o)|sorelle))?(( (q\.m?\.?)| (quondam)| (vedova( di)?)) ([a-z]|'|Ã²ò)+( di)?( ([a-z]|'|Ã²ò)+)?)*( indivisi)?$", Word, re.IGNORECASE):
            NameEFratello.append((ListofTronquedplusnumber[0][i],ListofTronquedplusnumber[1][i]))     #e avec un point d'interrogation
        elif re.search("sic|\.{4,15}", Word, re.IGNORECASE):
            NameFlou.append((ListofTronquedplusnumber[0][i],ListofTronquedplusnumber[1][i]))
        elif re.search("^(|-|N\.)$|^possessore ignoto", Word, re.IGNORECASE):
            Irrelevant.append((ListofTronquedplusnumber[0][i],ListofTronquedplusnumber[1][i]))
        else:
            Other.append((ListofTronquedplusnumber[0][i],ListofTronquedplusnumber[1][i]))

        Result = [("NomSeul", NameSolo),("NomEtQuondam",NameQuondam),("NomAvecFamille",NameEFratello),("NomDesEglises",Chiesa),
            ("Venezia", Venezia),("Demanio",Demanio),("other",Other)]        
    
    return Result 

# %%
with open(s0_list_of_tronques,) as f:
 countedTronqued = json.load(f)

def from_countedTronqued_to_print(countedTronqued):

    length = len(countedTronqued) #vaut 11624 au total

    other = []
    othSum = 0
    venezia = []
    venSum = 0
    demanio = []
    demSum = 0
    chiesa = []
    chiSum = 0
    congregazione = []
    conSum = 0
    name = []
    nameSolo = []
    solSum = 0
    nameEFratello = []
    fraSum = 0
    nameQuondam = []
    quoSum = 0
    nameFlou = []
    nameFlouSum = 0
    irrelevant = []
    irrSum = 0

    nomEnRegex = "([a-z]|')+ [a-z]{0,15}( di)? ?[a-z]{0,15}(e fratell(i|o))?"

    for i in range(length):
        word = countedTronqued[i][1]
        if re.search("(citt..|comm?une) di venezia|cimiterio|^patriarcato di venezia", word, re.IGNORECASE) is not None:
            venezia.append(countedTronqued[i])
            venSum += countedTronqued[i][0]
        elif re.search("(regio )?deman(i|e)o|ministe?ro|reale corona|tesoro", word, re.IGNORECASE) is not None:
            demanio.append(countedTronqued[i])
            demSum += countedTronqued[i][0]
        elif re.search("chiesa|monastero|benefi(c|z)io|^capitolo|^prebenda", word, re.IGNORECASE): #capitolo,prebende, beneficio
            chiesa.append(countedTronqued[i])
            chiSum += countedTronqued[i][0]
        elif re.search("congregazione", word, re.IGNORECASE):
            congregazione.append(countedTronqued[i])
            conSum += countedTronqued[i][0]
        elif re.search("^(eredi del fu )?([a-z]|'|Ã²|ò)+ ?(([a-z]|Ã²|ò)+ )?(di )?([a-z]|Ã²|ò)+ *$", word, re.IGNORECASE):
            nameSolo.append(countedTronqued[i])
            solSum += countedTronqued[i][0]
        elif re.search("^([a-z]|'|Ã²|ò)+( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²|ò)+)?( (q\.m?\.?|quondam|vedova( di)?)( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²|ò)+)?( (\.)+)?)+$",word,re.IGNORECASE):
            nameQuondam.append(countedTronqued[i])
            quoSum += countedTronqued[i][0]
        elif re.search("^([a-z]|'|Ã²|ò)+( ([a-z]|'|Ã²|ò)+)?( di)?( ([a-z]|'|Ã²ò)+)?( ed? ([a-z]|'|Ã²ò)+)?(( e)? (fratell(i|o)|sorelle))?(( (q\.m?\.?)| (quondam)| (vedova( di)?)) ([a-z]|'|Ã²ò)+( di)?( ([a-z]|'|Ã²ò)+)?)*( indivisi)?$", word, re.IGNORECASE):
            nameEFratello.append(countedTronqued[i])     #e avec un point d'interrogation
            fraSum += countedTronqued[i][0]
        elif re.search("sic|\.{4,15}", word, re.IGNORECASE):
            nameFlou.append(countedTronqued[i])
            nameFlouSum += countedTronqued[i][0]
        elif re.search("^(|-|N\.)$", word, re.IGNORECASE):
            irrelevant.append(countedTronqued[i])
            irrSum += countedTronqued[i][0]
        else:
            other.append(countedTronqued[i])
            othSum += countedTronqued[i][0]

    "eredi del fu"
    "^([a-z]|')+ ([a-z])+$"
    "( (ed?|q\.m?\.?|quondam) ([a-z]|')+ ?[a-z]{0,15}( di)? ?[a-z]{0,15}(e fratell(i|o))?)*"

    print("Venise : noms = ",len(venezia), " parcelles = ", venSum,
        "\nDemanio : noms = ", len(demanio), " parcelles = ", demSum,
        "\nchiesa : noms = ", len(chiesa), " parcelles = ", chiSum,
        "\nCongregazione : noms = ", len(congregazione), " parcelles = ", conSum,
        "\nNomSeul : noms = ", len(nameSolo), " parcelles = ", solSum,
        "\nE fratellio : noms = ", len(nameEFratello), "parcelles = ", fraSum,
        "\nseul avec Quondam = ", len(nameQuondam), " parcelles = ", quoSum,
        "\nnom flou = ", len(nameFlou), "parcelles = ", nameFlouSum,
        "\nirrelevant = ", len(irrelevant), "parcelles = ", irrSum,
        "\nAutres : noms = ", len(other), " parcelles = ", othSum,
        "\nTotaux : noms = ", length, "parcelles = 22691") 
    len(other)


    nb_noms = (len(venezia), len(demanio), len(chiesa), len(congregazione), len(nameSolo),
        len(nameEFratello), len(nameQuondam), len(nameFlou), len(irrelevant), len(other))
    nb_parcelles = (venSum, demSum, chiSum, conSum, solSum, fraSum, quoSum, nameFlouSum, irrSum, othSum)
    nb_cat = len(nb_noms)

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(nb_cat)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, nb_noms, bar_width,
    alpha=opacity,
    color='b',
    label='nombre d\'entrée  avec des noms différents')

    rects2 = plt.bar(index + bar_width, nb_parcelles, bar_width,
    alpha=opacity,
    color='g',
    label='nombre de parcelles')

    plt.xlabel('type de propriétaire')
    plt.ylabel('nombre')
    plt.title('répartition des propriétaires par type')
    plt.xticks(index + bar_width, ('venezia', 'demanio', 'chiesa', 'congreg.','nom seul', 'famille',
        'quondam','sic','non pertinent', 'autres' ), rotation=40)
    plt.legend()

    plt.tight_layout()
    plt.show()
# %%