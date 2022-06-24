#%%
import json
import re
import nltk
import matplotlib.pyplot as plt

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from data_filepaths import s0_raw_sommarioni
from s0_list_of_terms.function_lists import from_sommarioni_to_texts
from s1_classification.functions_classification import from_texts_to_listByType,from_listByType_to_barChart

from s2_extraction.fe import dahux
print("dahux!!!s")
print(dahux)


#%%
with open(s0_raw_sommarioni,encoding="utf-8") as f:
    sommarioni = json.load(f)

texts = from_sommarioni_to_texts(sommarioni)
listByType = from_texts_to_listByType(texts)

#%%
from_listByType_to_barChart(listByType)

# %%
