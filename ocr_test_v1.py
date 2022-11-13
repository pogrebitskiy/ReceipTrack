# text recognition
import cv2
import pytesseract
from receipt_class import Receipt
import datetime
import re

# read image
img = cv2.imread('target_receipt.png', 0)
# configurations
config = ('-l eng --oem 1 --psm 6')

text = pytesseract.image_to_string(img, config=config, lang='eng')

r1 = Receipt(text)
#print(r1.str_lst)
r1.get_totals()
print(r1.subtotal)