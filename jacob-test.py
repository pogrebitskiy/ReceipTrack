from PIL import Image
import requests
import pytesseract
import cv2
import numpy as np
from pytesseract import Output
import re
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jakul\anaconda3\Library\bin\tesseract.exe'

img = cv2.imread('receipt-ocr-original.jpg')
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img= cv2.fastNlMeansDenoising(img, None, 20, 7, 21)
img = cv2.fastNlMeansDenoisingColored(img,None,20,20,7,21)

custom_config = r'-l eng --oem 3 --psm 6'
text = pytesseract.image_to_string(img, config=custom_config, lang='eng')
print(text)
