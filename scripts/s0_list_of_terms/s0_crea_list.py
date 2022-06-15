# %%

import json
import re

import sys

sys.path.append("../../src")
sys.path.append("../../scripts")
sys.path.append("../../scripts/s0_list_of_terms")

from data_filepaths import s0_raw_sommarioni
from data_filepaths import s0_list_of_terms
from data_filepaths import s0_owners_texts
from data_filepaths import s0_texts_plus_parcels
from data_filepaths import s0_bigrams

from s0_list_of_terms.function_lists import from_sommarioni_to_list_of_terms,from_sommarioni_to_texts,from_sommarioni_to_texts_plus_parcelNumber,from_sommarioni_to_bigrams
# %%
with open(s0_raw_sommarioni,encoding="utf-8") as f:
    sommarioni = json.load(f)

#%%
list_of_terms = from_sommarioni_to_list_of_terms(sommarioni)

list_of_terms_json = json.dumps(list_of_terms)
with open(s0_list_of_terms, "w", encoding="utf-8") as w:
    w.write(list_of_terms_json)


# %%
list_of_texts = from_sommarioni_to_texts(sommarioni)

list_of_texts_json = json.dumps(list_of_texts)
with open(s0_owners_texts, "w")as w:
    w.write(list_of_texts_json)

# %%
list_plus_parcelles = from_sommarioni_to_texts_plus_parcelNumber(sommarioni)

list_plus_parcelles_json = json.dumps(list_plus_parcelles)
with open(s0_texts_plus_parcels, "w") as w:
    w.write(list_plus_parcelles_json)

#%%
bigrams = from_sommarioni_to_bigrams(sommarioni)

birgrams_json = json.dumps(bigrams)
with open(s0_bigrams, "w") as w:
    w.write(birgrams_json)
# %%
