# %%

from os.path import join as j

relative_path_to_root = j("..","..")

# use and abuse from os.path.join() (here aliased as "j") it ensures cross OS compatible paths
data_folder = j(relative_path_to_root, "data")
scripts_folder = j(relative_path_to_root, "scripts")
figures_folder = j(relative_path_to_root, "report", "figures")

# STEP 0 List of terms
# ===================================

s0_folder = j(data_folder, "s0_list_of_terms")
s0_raw_sommarioni = j(s0_folder, "sommarioni.json")
s0_list_of_terms = j(s0_folder, "listOfTerms.json")
s0_list_of_tronques = j(s0_folder, "listOfTronques.json")
s0_terms_only = j(s0_folder, "termsOnly.json")
s0_tronquesRaw = j(s0_folder, "tronquesRaw.json")
s0_list_plus_parcelles = j(s0_folder, "listOfTronqPlusParcelles.json")

s1_folder = j(data_folder, "s1_regex")
s1_bigrams = j(s1_folder, "s1_bigrams.json")

s2_folder = j(data_folder, "s2_list_de_proprietaires")
s2_setPrenoms = j(s2_folder,"setPrenoms.json")
s2_setFamilles = j(s2_folder,"setFamilles.json")

s0_scriptsDos = j(scripts_folder, "s0_list_of_terms")
s0_scripts = j(s0_scriptsDos, "s0_list_of_terms.py")


# %%
