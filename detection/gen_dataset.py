import cv2
import imgaug
import shapely
import os

bg_list = []
path = "./detection/dtd/images/"
bg_folders = os.listdir(path)

for folder in bg_folders:
    bg_list += [path + folder + "/" + f  for f in os.listdir(path + folder) if os.path.isfile(path + folder + "/" + f)]

print(len(bg_list))

# Display a bg

# Display a card in a 2nd window

# modify the cards

# create a scene in the background

# scene -> yolo labels

# serialize background

# create scene from serial

# generate lot of random serial and process them

# run the training!
