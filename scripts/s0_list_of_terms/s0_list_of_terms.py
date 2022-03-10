# %%

import json

# adds scripts/ and src/ folder: so you can import scripts/functions across project steps
import sys 
sys.path.append("../../src")
sys.path.append("../../scripts")

# import data filepath we want to use
from data_filepaths import s0_raw_sommarioni
print(s0_raw_sommarioni)

# %%

with open(s0_raw_sommarioni,) as f:
    sommarioni = json.load(f)
#print(sommarioni[0])
print(sommarioni[0]['parcelOwnerText'])
parcelOwnerTexts = [line['parcelOwnerText'] for line in sommarioni]
print(parcelOwnerTexts[0:5])
#print(sommarioni['parcelOwnerText'])
# %%
