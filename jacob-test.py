from PIL import Image
import requests
import pytesseract
import cv2
import numpy as np
from pytesseract import Output
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jakul\anaconda3\Library\bin\tesseract.exe'

image = Image.open('receipt-ocr-original.jpg')
#image = image.resize((300,150))
print(image)

custom_config = r'-l eng --oem 3 --psm 6'
text =pytesseract.image_to_string(image) # ERROR HERE
print(text)
