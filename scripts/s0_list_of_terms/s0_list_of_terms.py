# %%

import json
import re

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
#print(s0_raw_sommarioni)

# %%
with open(s0_raw_sommarioni,) as f:
    sommarioni = json.load(f)

parcelOwnerTexts = [line['parcelOwnerText'] for line in sommarioni]

length = len(parcelOwnerTexts)


splited = []
for i in range(length):
    if (parcelOwnerTexts[i] is not None):
        #for word in parcelOwnerTexts[i].replace("[",'').replace("]",'').replace(",",'').split(" "):
        wordsubbed = re.sub("\[|\]|,|'|\s+$","", parcelOwnerTexts[i])
        for word in re.split("\s",wordsubbed):
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


# %%
"""
tronqued = []
for i in range(length):
    if (parcelOwnerTexts[i] is not None):
    #splited[i] = parcelOwnerTexts[i].split(" ")
        #word = parcelOwnerTexts[i].replace("[",'').replace("]",'').replace("Suddetti",'').replace("Suddetto",'').replace(" ",'')
        word = re.sub("\[|\]|,|'|\s+$|(s|S)uddett(a|o|i)","", parcelOwnerTexts[i])
        tronqued.append(word)


nameset_2 = set(tronqued)
counted2 =[(tronqued.count(name),name) for name in nameset_2]
counted2.sort()
#sorted2 = sorted(counted2)
print(counted2)

counted2_json = json.dumps(counted2)
with open(s0_list_of_tronques, "w") as w:
    w.write(counted2_json)
"""

# %%
