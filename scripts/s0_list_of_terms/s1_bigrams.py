
from s0_crea_list import *

#%%
bigrams = from_sommarioni_to_bigrams(sommarioni)

birgrams_json = json.dumps(bigrams)
with open(s0_bigrams, "w") as w:
    w.write(birgrams_json)
# %%
