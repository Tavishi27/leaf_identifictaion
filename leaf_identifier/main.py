'''
Tavishi Bhatia
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
