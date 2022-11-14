from PIL import Image
import requests
import pytesseract
import cv2
import numpy as np
from pytesseract import Output
import re
import cv2
from receipt_class import Receipt
import datetime
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jakul\anaconda3\Library\bin\tesseract.exe'

img = cv2.imread('receipt-ocr-original.jpg')
img= cv2.fastNlMeansDenoising(img, None, 20, 7, 21)
img = cv2.fastNlMeansDenoisingColored(img,None,20,20,7,21)

custom_config = r'-l eng --oem 3 --psm 6'
text = pytesseract.image_to_string(img, config=custom_config, lang='eng')

r1 = Receipt(text)
#print(r1.str_lst)
r1.get_totals()
r1.get_date()
r1.get_phone()
print(r1)
