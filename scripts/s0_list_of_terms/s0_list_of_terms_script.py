# %%

import json
import re
import spacy

import pandas
#pandas._version_

# adds scripts/ and src/ folder: so you can import scripts/functions across project steps
import sys 
sys.path.append("../../src")
sys.path.append("../../scripts")

# import data filepath we want to use
from data_filepaths import s0_raw_sommarioni
from data_filepaths import s0_list_of_terms
from data_filepaths import s0_list_of_tronques
#from data_filepaths import s0_tronquesRaw
#from data_filepaths import s0_terms_only
#print(s0_raw_sommarioni)


#%%

#prend en input fichier json loadé et en resort la liste des owner sans les suddeti et triée
def from_sommarioni_to_countedTronqued(Sommarioni):

    ParcelOwnerTexts = [line['parcelOwnerText'] for line in Sommarioni]

    Length = len(ParcelOwnerTexts)

    Tronqued = []
    for i in range(Length):
        if (ParcelOwnerTexts[i] is not None):
            Word = re.sub("\[|\]|,| +$|^ +| ?(s|S)(u|U)ddett(e|a|o|i)| *$","", ParcelOwnerTexts[i])
            Word2 = re.sub("\u00e0","à",Word)
            Word3 = re.sub("\u00f2","ò",Word2)
            Word4 = re.sub("\u00e8","è",Word3)
            Tronqued.append(Word4)

    Nameset_2 = set(Tronqued)
    
    Counted = [(Tronqued.count(Name),Name) for Name in Nameset_2]
    Counted.sort()
    return Counted
# %%
def from_sommarioni_to_Tronqued_plus_parcelNumber(Sommarioni):
    ParcelOwnerTexts = [line['parcelOwnerText'] for line in Sommarioni]

    Length = len(ParcelOwnerTexts)

    Result = [[],[]]
    for i in range(Length):
        if (ParcelOwnerTexts[i] is not None):
            Word = re.sub("\[|\]|,| +$|^ +| ?(s|S)(u|U)ddett(e|a|o|i)| *$","", ParcelOwnerTexts[i])
            if Word in Result[0]:
                index = Result[0].index(Word)
                Result[1][index].append(i)
            else :
                Result[0].append(Word)
                Result[1].append([i])
    
    return Result

# %%
with open(s0_raw_sommarioni,) as f:
    sommarioni = json.load(f)

parcelOwnerTexts = [line['parcelOwnerText'] for line in sommarioni]
#print(parcelOwnerTexts)
length = len(parcelOwnerTexts)

from_sommarioni_to_Tronqued_plus_parcelNumber(parcelOwnerTexts)

#%%
"""
splited = []
for i in range(length):
    if (parcelOwnerTexts[i] is not None):
        #for word in parcelOwnerTexts[i].replace("[",'').replace("]",'').replace(",",'').split(" "):
        wordsubbed = re.sub("\[|\]|,|'|\s+$","", parcelOwnerTexts[i])
        Word2 = re.sub("\u00c3","à",wordsubbed)
        Word3 = re.sub("\u00c3\u00b2","ò",Word2)
        Word4 = re.sub("\u00c3\u2030","é",Word3)
        Word5 = re.sub("\u00c3\u00a8","è",Word4)
        for word in re.split("\s",Word5):
        #print(wordsplited)
            splited.append(word)

print(splited)
nameset = set(splited)

#counted={name:splited.count(name) for name in nameset}
counted1=[(splited.count(name),name) for name in nameset]
#sorted1 = sorted(counted1)
counted1.sort()
print(counted1)

counted1_json = json.dumps(counted1)
with open(s0_list_of_terms, "w") as w:
    w.write(counted1_json)
"""

# %%

tronqued = []
for i in range(length):
    if (parcelOwnerTexts[i] is not None):
    #splited[i] = parcelOwnerTexts[i].split(" ")
        #word = parcelOwnerTexts[i].replace("[",'').replace("]",'').replace("Suddetti",'').replace("Suddetto",'').replace(" ",'')
        #!!!!!!!!!!!!!!!!!attention suddetto des fois seul, à changer
        word = re.sub("\[|\]|,| +$| +^|(s|S)(u|U)ddett?(e|a|o|i) *","", parcelOwnerTexts[i])
        word2 = re.sub("\u00e0","à",word)
        word3 = re.sub("\u00f2","ò",word2)
        word4 = re.sub("\u00e8","è",word3)
        tronqued.append(word4)

nameset_2 = set(tronqued)

counted2 =[(tronqued.count(name),name) for name in nameset_2]
counted2.sort()
#sorted2 = sorted(counted2)


print(counted2)


counted2_json = json.dumps(counted2)
with open(s0_list_of_tronques, "w") as w:
    w.write(counted2_json)


# %%
