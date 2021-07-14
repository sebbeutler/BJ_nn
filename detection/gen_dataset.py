import cv2
import imgaug
import shapely
import os
import random
import imgaug as ia
import imgaug.augmenters as iaa
import numpy as np
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage

def boundingBoxesToLabel(size, bbs, card_ids):
    # yolo labels : id x_center y_center width height (all 0-1)
    result = ""
    for i in range(len(card_ids)):
        x_center = (bbs[i].x1 + (bbs[i].x2 - bbs[i].x1)/2) / size[0]
        y_center = (bbs[i].y1 + (bbs[i].y2 - bbs[i].y1)/2) / size[1]
        width = (bbs[i].x2 - bbs[i].x1) / size[0]
        height = (bbs[i].y2 - bbs[i].y1) / size[1]
        result += " ".join(list(map(str, [card_ids[i], x_center, y_center, width, height]))) + "\n"
    return result

# Gather all the path to background images
bg_size = (608,608)

bg_list = []
path = "./detection/dtd/images/"
output_path = "./detection/training_set/"
bg_folders = os.listdir(path)

for folder in bg_folders:
    bg_list += [path + folder + "/" + f  for f in os.listdir(path + folder) if os.path.isfile(path + folder + "/" + f)]

# Gather all cards names
card_list = ["QT", "8Ca"]

ia.seed(2121212121)

aug_seq = iaa.Sequential([
    iaa.Fliplr(0.5), # horizontal flips
    iaa.Affine(
        scale={"x": (0.3, 1), "y": (0.3, 1)},
        rotate=(-180,180),
        shear=(-8, 8),
        translate_percent={"x":(-0.25,0.25),"y":(-0.25,0.25)}
    ),
    iaa.PerspectiveTransform(scale=(0.01, 0.15)),
    iaa.Sometimes(
        0.5,
        iaa.GaussianBlur(sigma=(0, 0.5))
    ),
    iaa.Multiply((0.8, 1.2), per_channel=0.2)
], random_order=True) # apply augmenters in random order


# Superpose card image with the background


max_card = 4
output_count = len(bg_list)

traintxt = open(output_path + "/train.txt", "a")

for i in range(output_count):
    # Select a random background
    bg_img_name = bg_list[i]
    bg_img = cv2.resize(cv2.imread(bg_img_name), bg_size, interpolation=cv2.INTER_AREA)
    aug_bbs = []
    cards_list =[]
    final = bg_img
    for j in range(random.randint(1, max_card)):
        cards_list.append(random.randint(0, len(card_list)-1))
        card_img = cv2.imread("./detection/card_set/" + card_list[cards_list[-1]] + ".png")
        resized_card = np.zeros_like(bg_img, dtype='uint8')
        x_offset=int((bg_size[0]-card_img.shape[1])/2)
        y_offset=int((bg_size[1]-card_img.shape[0])/2)
        resized_card[y_offset:y_offset+card_img.shape[0], x_offset:x_offset+card_img.shape[1]] = card_img
        image_aug, bbs_aug = aug_seq(image=resized_card, bounding_boxes=[BoundingBox(x_offset, y_offset, x_offset+card_img.shape[1], y_offset+card_img.shape[0])])
        aug_bbs.append(bbs_aug[0])
        final=np.where(image_aug,image_aug,final)

    cv2.imwrite(output_path + bg_img_name.split("/")[-1], final)

    with open(output_path + bg_img_name.split("/")[-1][:-4] + ".txt", 'w') as f:
        f.write(boundingBoxesToLabel(bg_size, aug_bbs, cards_list))

    traintxt.write("C:\\D\\Desktop\\projects\\BJ\\detection\\training_set\\" + bg_img_name.split("/")[-1] + "\n")

    print("Generating . . . (" + str(i+1) + "/" + str(output_count) + ")")


# create a scene in the background

# scene -> yolo labels

# create random scenes

# serialize generation

# create scene from serial

# generate lot of random serial and process them

# run the training!
