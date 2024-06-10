'''
Tavishi Bhatia
5/7/24

Program uses a trained YOLO v8 image classification model to classify provided leaf images
'''

from ultralytics import YOLO
import pandas as pd


# classify() takes an image path and uses a trained model to classify the image
# and return's a prediction of the image's scientific name, common name, and confidence percentage
def classify(img):
    # load the trained model
    model = YOLO("./train4/weights/last.pt")
    results = model(img)

    # get the probabilities of the image fitting into that category for each leaf
    names_dict = results[0].names
    probs = results[0].probs.tolist()
    # get the species with the highest probability
    max_prob = 0
    max_prob_index = 0
    for n in range(0, len(probs)):
        if probs[n] > max_prob:
            max_prob = probs[n]
            max_prob_index = n
    # convert the probability to a percentage
    percent = round(max_prob * 100, 2)

    # use leaves.csv to get the tree's common name
    common_names = pd.read_csv("leaves.csv")
    # format the scientific name
    scientific_name = names_dict[max_prob_index].replace("_", " ").capitalize()
    common_name = common_names[common_names["species"] == scientific_name].common_name.to_list()[0]

    return scientific_name, common_name, percent
