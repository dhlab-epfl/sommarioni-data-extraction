# %%

import json
import re
import spacy
import nltk
#nltk.download('punkt')

#%%
def from_sommarioni_to_bigrams(sommarioni):
    """ This function does this and that
    
    parameters:
    - sommarioni

    returns
    - something
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
    counted.sort()
    print(counted)

    return counted

# %%
