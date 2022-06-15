# %%

import json
import re
import nltk

# adds scripts/ and src/ folder: so you can import scripts/functions across project steps
import sys 
sys.path.append("../../src")
sys.path.append("../../scripts")

#%%

#prend en input fichier json loadé et en resort la liste des owner sans les suddeti et triée
def from_sommarioni_to_texts(sommarioni):
    '''
    Remplace les suddetto par les propriétaires véritables, supprime la ponctuation
    Associe chaque textes possibles (entrée) présentes dans ParcelOwnerTexts avec le nombre de fois où ils apparaissent

            Parameters:
                    sommarioni (tableau json loadé): Les sommarioni    

            Returns:
                    counted (liste de tuples (int, string)): la liste des entrées et leur nombre d'occurrences
                    
    '''

    parcelOwnerTexts = [line['parcelOwnerText'] for line in sommarioni]

    length = len(parcelOwnerTexts)

    texts = []
    for i in range(length):
        if (parcelOwnerTexts[i] is not None):
            Word = re.sub("\[|\]|,| +$|^ +| ?(s|S)(u|U)ddett(e|a|o|i)| *$","", parcelOwnerTexts[i])
            Word2 = re.sub("\u00e0","à",Word)
            Word3 = re.sub("\u00f2","ò",Word2)
            Word4 = re.sub("\u00e8","è",Word3)
            texts.append(Word4)

    textSet = set(texts)
    
    counted = [(texts.count(text),text) for text in textSet]
    counted.sort()
    return counted
# %%
def from_sommarioni_to_texts_plus_parcelNumber(sommarioni):
    """
    Remplace les suddetto par les propriétaires véritable, supprime la ponctuation 
    Associe chaque texte possible (entrée) dans ParcelOwnerTexts avec les id des parcelles possédées par cette entrées.

        Paramètre :
            sommarioni (liste) : le sommarioni
        Retourne :
            result ( [list de String, liste de liste d'integer] ): la liste des entrées chacune associée aux parcelles qu'elle possède (se situe au même index dans les deux listes principales) 
    
    """
    parcelOwnerTexts = [line['parcelOwnerText'] for line in sommarioni]

    length = len(parcelOwnerTexts)

    result = [[],[]]
    for i in range(length):
        if (parcelOwnerTexts[i] is not None):
            text = re.sub("\[|\]|,| +$|^ +| ?(s|S)(u|U)ddett(e|a|o|i)| *$","", parcelOwnerTexts[i])
            if text in result[0]:
                index = result[0].index(text)
                result[1][index].append(i)
            else :
                result[0].append(text)
                result[1].append([i])
    
    return result

#%%
def from_sommarioni_to_list_of_terms(Sommarioni):
    """
    Supprime quelques ponctuation, 
    Associe chaque mot présent dans les textes (terme) dans les textes avec le nombre de fois où il apparait 
        paramètre :
            sommarioni : le sommarioni
        retourne :
            counted (list de tuplet(string, int)) : list des terme et leur nombre d'occurence 
    
    
    """
    parcelOwnerTexts = [line['parcelOwnerText'] for line in Sommarioni]

    length = len(parcelOwnerTexts)

    splited = []
    for i in range(length):
        if (parcelOwnerTexts[i] is not None):
            #for word in parcelOwnerTexts[i].replace("[",'').replace("]",'').replace(",",'').split(" "):
            wordsubbed = re.sub("\[|\]|,|\s+$","", parcelOwnerTexts[i])
            Word2 = re.sub("\u00c3","à",wordsubbed)
            Word3 = re.sub("\u00c3\u00b2","ò",Word2)
            Word4 = re.sub("\u00c3\u2030","é",Word3)
            Word5 = re.sub("\u00c3\u00a8","è",Word4)
            for word in re.split("\s",Word5):
            #print(wordsplited)
                splited.append(word)

            #print(splited)
    wordset = set(splited)
    print('il y a ',len(wordset),' termes différents')

    #counted={name:splited.count(name) for name in nameset}
    counted=[(splited.count(word),word) for word in wordset]
    #sorted1 = sorted(counted1)
    counted.sort()
    return counted

# %%
def from_sommarioni_to_bigrams(sommarioni):
    """
    Remplace les suddetto par les propriétaires véritable, supprime la ponctuation,
    Associe chaque bigrammes présent dans les textes avec le nombre de fois où il aparait
        paramètre :
            sommarioni : le sommarioni
        retourne : 
            counted (list de tuplet (int,(string,string)) : la liste des bigrammes et leur nombre d'occurence
    """
    parcelOwnerTexts = [line['parcelOwnerText'] for line in sommarioni]

    length = len(parcelOwnerTexts)

    bigrams_full_list = []

    for i in range(length):
        if (parcelOwnerTexts[i] is not None):
            #word = parcelOwnerTexts[i].replace("[",'').replace("]",'').replace("Suddetti",'').replace("Suddetto",'').replace(" ",'')
            word = re.sub("\[|\]|,| +$| +^|(s|S)(u|U)ddett(e|a|o|i)","", parcelOwnerTexts[i])
            nltk_tokens = nltk.word_tokenize(word)
            for bigram in list(nltk.bigrams(nltk_tokens)):
                if ((re.search("(q\.m?\.?|quondam)",bigram[0]) is None) & (re.search("(q\.m?\.?|quondam)",bigram[1]) is None)): 
                    bigrams_full_list.append(bigram)


    bigramset = set(bigrams_full_list)

    counted=[(bigrams_full_list.count(name),name) for name in bigramset]
    counted.sort(reverse=True)

    return counted


# %%
