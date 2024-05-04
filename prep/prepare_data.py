'''
4/22/2024
Uses pandas and splitfolders to sort through and prepare the leaf dataset
'''

import pandas as pd
import splitfolders


# change leafsnap-dataset-images.txt file into a csv file to make it easier to work with
with open("leafsnap-dataset-images.txt", "r") as data:
    txt = data.read()
    edited_text = txt.replace("	", ",")
    with open("dataset.csv", "w") as new_data:
        new_data.write(edited_text)

# get list of all plant species in dataset
leaf_data = pd.read_csv("dataset.csv")
leaf_list = list(set(leaf_data.species.tolist()))
print(leaf_list)

# create csv file with each leaf and its corresponding common name
species_list = leaf_data.species.drop_duplicates().to_list()
for n in range(0, len(species_list)):
    species_list[n] = species_list[n].replace(" ", "_").lower()
ser = pd.Series(species_list)
ser.to_csv("leaf_species.csv")


# check leaves.csv file for duplicates or errors
common_names = pd.read_csv("leaves.csv")
print(common_names[["species", "common_name"]])
common_names["common_name"].duplicated().to_csv("check_for_duplicates.csv")

# use leaves.csv to add a common name column to dataset.csv
common_name_list = []
for index, row in leaf_data.iterrows():
    species = row["species"]
    common_name = common_names[common_names["species"] == species].common_name.to_list()[0]
    common_name_list.append(common_name)
leaf_data.insert(4, "common_name", common_name_list, True)
leaf_data.set_index("file_id", inplace=True)
leaf_data.to_csv("dataset.csv")

# split data into train and val folders for Yolov8 model
splitfolders.ratio(input="/Users/tavis/OneDrive/Desktop/Leaf Identification/data/leafsnap-dataset/dataset/images/field", output="split_data",
                   seed=1337, ratio=(.8, .2, 0), group_prefix=None, move=False)

