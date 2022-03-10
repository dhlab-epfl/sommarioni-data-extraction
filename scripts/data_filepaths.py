# %%

from os.path import join as j

relative_path_to_root = j("..","..")

# use and abuse from os.path.join() (here aliased as "j") it ensures cross OS compatible paths
data_folder = j(relative_path_to_root, "data")
figures_folder = j(relative_path_to_root, "report", "figures")

# STEP 0 List of terms
# ===================================

s0_folder = j(data_folder, "s0_list_of_terms")
s0_raw_sommarioni = j(s0_folder, "sommarioni.json")




# %%
