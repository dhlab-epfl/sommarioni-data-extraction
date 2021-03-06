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
s0_list_of_terms = j(s0_folder, "terms.json")
s0_owners_texts = j(s0_folder, "ownersTexts.json")
s0_texts_plus_parcels = j(s0_folder, "textsPlusParcels.json")
s0_bigrams = j(s0_folder, "bigrams.json")

s2_folder = j(data_folder, "s2_extraction")
s2_setPrenoms = j(s2_folder,"setPrenoms.json")
s2_setFamilles = j(s2_folder,"setFamilles.json")

s0_scriptsDos = j(scripts_folder, "s0_list_of_terms")
s0_scripts = j(s0_scriptsDos, "s0_list_of_terms.py")


# %%
