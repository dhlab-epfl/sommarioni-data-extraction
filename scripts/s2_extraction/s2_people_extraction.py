#%%
import json
import re

import sys

#from scripts.s2_list_de_proprietaires.s2_listDesPersonnes import gestion_nom_seul
sys.path.append("../../src")
sys.path.append("../../scripts")


from s0_list_of_terms.function_lists import from_sommarioni_to_texts_plus_parcelNumber
from s1_classification.functions_classification import from_textsPlusParcels_to_listBytype
from s2_extraction.functions_extraction import gestion_nom_seul, gestion_avec_quondam, gestion_avec_famille

from data_filepaths import s0_raw_sommarioni

#%%
with open(s0_raw_sommarioni,encoding="utf-8") as f:
    sommarioni = json.load(f)

#%%
texts_plus_parcelsNumber = from_sommarioni_to_texts_plus_parcelNumber(sommarioni)

# %%
listByType_plusNumber = from_textsPlusParcels_to_listBytype(texts_plus_parcelsNumber)

# %%
nomSeul=listByType_plusNumber[4][1]
nomAvecQuondam=listByType_plusNumber[5][1]
nomAvecFamille = listByType_plusNumber[6][1]
#%%
#gestion des nom seul
personneSeul, parcelesSeul, nonClasseeSeul = gestion_nom_seul(nomSeul, aff_result=True)

#%%
#gestion des nom avec quondam
personnesQuondam, parcellesQuondam, nonClasseeQuondam = gestion_avec_quondam(nomAvecQuondam, aff_result=True)

#%%
#gestion des nom avec famille
personnesFamille, parcellesFamille, nonClasseeFamille = gestion_avec_famille(nomAvecFamille, aff_result=True)

# %%
