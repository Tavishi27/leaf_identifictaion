'''
Tavishi Bhatia'''
Tavishi Bhatia
5/14/24

Program shows the user a tkinter window that prompts them to upload an image.
The program will then classify that image using a trained sklearn model and provide a description
about the tree in the predicted classification.
'''

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import predict
import wikipedia_summary
import pandas as pd
import math
import pyperclip


# upload_image() is run when the user presses the upload image button
# allows the user to upload an image
def upload_image():
    # only allow jpg and jpeg files
    file_name = filedialog.askopenfilename(filetypes=[("Jpg files", ".jpg"), ("Jpeg files", ".jpeg")])
    # format file path
    file_name = file_name[file_name.index("/"):]
    # assign the file path to the global variable img and display it
    global img
    img = file_name
    show_img()


# show_img() displays the image in the img variable on the screen
def show_img():
    global img, leaf_img
    # get rid of previous leaf image, label, description, source, and copy link button
    leaf_img.pack_forget()
    clear_screen()

    # resize image if it's too big to display
    im = Image.open(img)
    width, height = im.size
    while width > max_width or height > max_height:
        im = Image.open(img)
        new_size = (int(width / 2), int(height / 2))
        im = im.resize(new_size)
        im.save("./adjusted_imgs/new_img.jpg")
        img = "./adjusted_imgs/new_img.jpg"
        im = Image.open(img)
        width, height = im.size

    # format the image as a PhotoImage and display it as a label
    uploaded_img = ImageTk.PhotoImage(Image.open(img))
    panel = tk.Label(screen, image=uploaded_img, background=bg_color)
    panel.image = uploaded_img  # not sure what this line does but the img doesn't show up without it
    panel.pack()
    leaf_img = panel


# classify_img() is run when the user presses the classify image button
# uses predict to get and display the image's predicted scientific name, common name, and confidence score
def classify_img():
    global img, leaf_label, description_label, source_label, copy_link_button, link
    # get rid of previous leaf label, description label, source label, and copy link button
    clear_screen()

    # use predict to create a new leaf label
    scientific_name, common_name, percent = predict.classify(img)
    # some of the dataset's labels are outdated
    # so, if the leaf has an alternate (updated) name, display that instead
    # alternate names are recorded in leaves.csv
    leaves_data = pd.read_csv("leaves.csv")
    alt_name = leaves_data[leaves_data["species"] == scientific_name].alternate_name.to_list()[0]
    try:
        # the alternate name for trees without one is nan
        math.isnan(alt_name)
    except TypeError:
        name = alt_name
    else:
        name = scientific_name
    leaf_label = tk.Label(screen, text=name + " (" + common_name + ")\nConfidence score: " + str(percent) + "%",
                          font=(default_font_name, 11))
    leaf_label.pack()

    # use wikipedia_summary to create a new description label
    txt = wikipedia_summary.get_description(scientific_name)
    description_label = tk.Label(screen, text=txt, background=bg_color)
    description_label.pack()

    # write the url for the wikipedia page the tree description is from to create a new source label
    link = "https://en.wikipedia.org/wiki/" + name.replace(" ", "_")
    source_label = tk.Label(screen, text="Source: " + link, background=bg_color)
    source_label.pack()

    # create copy link button
    copy_link_button = tk.Button(screen, text="Copy Link", command=copy_link, background=button_color)
    copy_link_button.pack()


# copy_link() uses pyperclip to copy the link to the clipboard
def copy_link():
    pyperclip.copy(link)


# clear_screen() deletes the current leaf label, description label, source label, and copy link button
def clear_screen():
    leaf_label.pack_forget()
    description_label.pack_forget()
    source_label.pack_forget()
    copy_link_button.pack_forget()


# variables
bg_color = "LightSkyBlue1"
button_color = "snow"
max_height = 500
max_width = 500
padding = 40
default_font_name = "Segoe UI"
link = ""

# create and format the screen
screen = tk.Tk()
screen.title("Leaf Identifier")
screen.minsize(width=max_width, height=max_height)
screen.config(padx=padding, pady=padding, background=bg_color)


# create and format the title label
title_label = tk.Label(screen, text="Leaf Identifier", font=("Sitka Small Semibold", 24), background=bg_color)
title_label.pack()

# create and format the instruction label
instructions_label = tk.Label(screen, text="Please upload an image of a leaf on a white background",
                              background=bg_color)
instructions_label.pack()

# create and format the upload button
upload_button = tk.Button(screen, text='Upload Image', command=upload_image, background=button_color,
                          font=(default_font_name, 10))
upload_button.pack()

# create and format the classify image button
classify_img_button = tk.Button(screen, text="Classify Image", command=classify_img, background=button_color,
                                font=(default_font_name, 10))
classify_img_button.pack()

# create the leaf label
leaf_label = tk.Label()

# create the description label
description_label = tk.Label()

# create the source label
source_label = tk.Label()

# create the copy link button
copy_link_button = tk.Button()

# create and display the leaf img label
img = "insert_img_icon.png"
leaf_img = tk.Label()
show_img()

# display the screen
screen.mainloop()

5/14/24

Program shows the user a tkinter window that prompts them to upload an image.
The program will then classify that image using a trained sklearn model.
'''

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import predict


# upload_image() is run when the user presses the upload image button
# allows the user to upload an image
def upload_image():
    # only allow jpg and jpeg files
    file_name = filedialog.askopenfilename(filetypes=[("Jpg files", ".jpg"), ("Jpeg files", ".jpeg")])
    # format file path
    file_name = file_name[file_name.index("/"):]
    # assign the file path to the global variable img and display it
    global img
    img = file_name
    show_img()


# show_img() displays the image in the img variable on the screen
def show_img():
    global img, leaf_img, leaf_label
    # get rid of previous leaf image and label
    leaf_img.pack_forget()
    leaf_label.pack_forget()

    # resize image if it's too big to display
    im = Image.open(img)
    width, height = im.size
    while width > max_width or height > max_height:
        im = Image.open(img)
        new_size = (int(width / 2), int(height / 2))
        im = im.resize(new_size)
        im.save("./adjusted_imgs/new_img.jpg")
        img = "./adjusted_imgs/new_img.jpg"
        im = Image.open(img)
        width, height = im.size

    # format the image as a PhotoImage and display it as a label
    uploaded_img = ImageTk.PhotoImage(Image.open(img))
    panel = tk.Label(screen, image=uploaded_img, background=bg_color)
    panel.image = uploaded_img  # not sure what this line does but the img doesn't show up without it
    panel.pack()
    leaf_img = panel


# classify_img() is run when the user presses the classify image button
# uses predict to get and display the image's predicted scientific name, common name, and confidence score
def classify_img():
    global img, leaf_label
    # get rid of previous leaf label
    leaf_label.pack_forget()

    # use predict to create a new leaf label
    scientific_name, common_name, percent = predict.classify(img)
    leaf_label = tk.Label(screen, text=scientific_name + " (" + common_name + ")\nConfidence score: " + str(percent) + "%")
    leaf_label.pack()

# variables
bg_color = "LightSkyBlue1"
button_color = "snow"
max_height = 500
max_width = 500

# create and format the screen
screen = tk.Tk()
screen.title("Leaf Identifier")
screen.minsize(width=max_width, height=max_height)
screen.config(padx=20, pady=20, background=bg_color)

# create and format the title label
title_label = tk.Label(screen, text="Leaf Identifier", font=("Sitka Small Semibold", 24), background=bg_color)
title_label.pack()

# create and format the instruction label
instructions_label = tk.Label(screen, text="Please upload an image of a leaf on a white background", background=bg_color)
instructions_label.pack()

# create and format the upload button
upload_button = tk.Button(screen, text='Upload Image', command=upload_image, background=button_color)
upload_button.pack()

# create and format the classify image button
classify_img_button = tk.Button(screen, text="Classify Image", command=classify_img, background=button_color)
classify_img_button.pack()

# create the leaf label
leaf_label = tk.Label()

# create and display the leaf img label
img = "insert_img_icon.png"
leaf_img = tk.Label()
show_img()

# display the screen
screen.mainloop()
