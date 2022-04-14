# %%

import json
import re
import spacy
import nltk
#nltk.download('punkt')

from data_filepaths import s0_raw_sommarioni

with open(s0_raw_sommarioni,) as f:
    sommarioni = json.load(f)

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


nameset = set(bigrams_full_list)

counted1=[(bigrams_full_list.count(name),name) for name in nameset]
counted1.sort()

# %%
print(counted1)
# %%
