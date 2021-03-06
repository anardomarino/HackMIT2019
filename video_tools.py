#coding=utf-8

#need to import open cv and pip install pillow

from __future__ import unicode_literals
import cv2
import numpy as np

from recog import recog
from PIL import ImageFont, ImageDraw, Image  
from parse_label import parse_label
from change_lang import change_lang

frame_name = "frame.jpg" # name of the file for the frame to be saved

def draw_tracking_box(box, image):
    """
    draws a bounding box

    box: tuple of the bounding box in format x,y,x,h where x,y are the coordinates
         and w,h and the width and height of the box respectively
    """
    (x, y, w, h) = [int(v) for v in box]
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


def draw_translation(output_strings, location, image):

    #output_strings is list of english word, language, translated
    if len(output_strings[0]) > len(output_strings[2]):
        longer_word = output_strings[0]
    else:
        longer_word = output_strings[2]

    image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    image_pillow = Image.fromarray(image_rgb)

    draw = ImageDraw.Draw(image_pillow)  
    # use a truetype font  
    font = ImageFont.truetype("Arial Black.ttf", 15)  

    text_size = font.getsize(longer_word)
    rect_size = (text_size[0]+8, (text_size[1]+4)*2)
    rect = Image.new('RGBA', rect_size, "black")
    rect_draw = ImageDraw.Draw(rect)
    rect_draw.text((5, 0), output_strings[2], font=font, fill="#FFFFFF")
    rect_draw.text((5, text_size[1]), output_strings[0], font=font, fill="#808080")
    image_pillow.paste(rect, (location[0], location[1]-(text_size[1]*2+10)))
   
    # Draw the text  
    #draw.text(location, output_string, font=font) 

    return cv2.cvtColor(np.array(image_pillow), cv2.COLOR_RGB2BGR)


    # image will be a numpy array
    # location will be a tple
    # output ewill be string
    # https://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html
    # opencv draw reactangle
    # opencv write text
    # return the image

def translate(box, frame, language="es"):
    """
    performs the translation operation including 
        - saving and recognizing a give portion of the image (current_box or frame)
        - deciding which recognition is the best
        - returns the recognition and the translation
    """
    x,y,w,h = [int(p) for p in box] # convert the coordinates to integers
    cv2.imwrite(frame_name, frame[y:y+h,x:x+w]) # save image of just the 
    recognition_output = recog(frame_name) # run the image recognition
    to_translate = parse_label(recognition_output) # get the name of the object in english
    translated = change_lang(to_translate, language) # translate the object into specified language
    return to_translate, translated
