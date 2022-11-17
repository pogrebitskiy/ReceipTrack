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
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jakul\anaconda3\Library\bin\tesseract.exe'

receipts = []
os.chdir('./receipts/')
for file in os.listdir(os.getcwd()):
    img = cv2.imread(file)

    img = cv2.fastNlMeansDenoising(img, None, 20, 7, 21)
    img = cv2.fastNlMeansDenoisingColored(img, None, 20, 20, 7, 21)

    custom_config = r'-l eng --oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config, lang='eng')

    receipt = Receipt(text)
    receipt.get_totals()
    receipt.get_date()
    receipt.get_phone()
    receipt.change_due()
    receipts.append(receipt)

os.chdir('../')

print(receipts)