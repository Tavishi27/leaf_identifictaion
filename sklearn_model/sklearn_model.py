'''
4/29/2024
Trains an image classification model using sklearn
'''

import os
from skimage.io import imread
from skimage.transform import resize
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

# prepare data
# Enter image directory file path
input_dir = "/Users/tavis/OneDrive/Desktop/Leaf Identification/data/leafsnap-dataset/dataset/images/field"
# get categories from the leaf species csv file
categories = pd.read_csv("leaf_species.csv")["species"].to_list()
#categories = ['abies_concolor', 'abies_nordmanniana', 'acer_campestre', 'acer_ginnala', 'acer_griseum', 'acer_palmatum', 'acer_platanoides', 'acer_pseudoplatanus', 'acer_rubrum', 'acer_saccharinum', 'acer_saccharum']
print("categories list has been acquired")

# create data and labels lists to train the model
data = []
labels = []
for category_idx, category in enumerate(categories):
    # deal with FileNotFoundErrors
    try:
        os.listdir(os.path.join(input_dir, category))
    except FileNotFoundError:
        print(category + " was skipped")
    else:
        for file in os.listdir(os.path.join(input_dir, category)):
            # prepare each image and append it to the data list
            img_path = os.path.join(input_dir, category, file)
            img = imread(img_path)
            img = resize(img, (15, 15))
            data.append(img.flatten())
            # append the index of the category of the image to the labels list
            labels.append(category_idx)
        print(category + " has been formatted")
print("all categories have been formatted")


# format the data and labels lists into a numpy array
data = np.asarray(data)
labels = np.asarray(labels)

# train / test split
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)
print("train / test split has been completed")

# train classifier
classifier = SVC()
# gammma is Kernel coefficient for rbf, poly and sigmoid.
# C is the regularization parameter.
# The strength of the regularization is inversely proportional to C. Must be strictly positive.
parameters = [{"gamma": [0.01, 0.001, 0.0001], "C":[1, 10, 100, 1000]}]
# parameters are used to train 12 different image classifiers with different gamma and C combinations
# grid_search creates and trains all 12 models
grid_search = GridSearchCV(classifier, parameters)
grid_search.fit(x_train, y_train)
print("model has been trained")

# test performance
# analyze the best performing model
best_estimator = grid_search.best_estimator_
y_prediction = best_estimator.predict(x_test)
score = accuracy_score(y_prediction, y_test)
print("{}% of samples were correctly classifies".format(str(score * 100)))

# save best_estimator model to "sklearn_model.pkl"
joblib.dump(best_estimator, "model.pkl", compress=3)

