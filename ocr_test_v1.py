# text recognition
import cv2
import pytesseract
from receipt_class import Receipt
import datetime
import re
import os

receipts = []
os.chdir('./receipts/')
for file in os.listdir(os.getcwd()):
    # read image
    img = cv2.imread(file, 0)
    # configurations
    config = ('-l eng --oem 1 --psm 6')

    text = pytesseract.image_to_string(img, config=config, lang='eng')

    receipt = Receipt(text)
    receipt.get_totals()
    receipt.get_date()
    receipt.get_phone()

    receipts.append(receipt)

os.chdir('../')

print(receipts[0])

'''
# read image
img = cv2.imread('./receipts/target_receipt.png', 0)
# configurations
config = ('-l eng --oem 1 --psm 6')

text = pytesseract.image_to_string(img, config=config, lang='eng')

r1 = Receipt(text)
#print(r1.str_lst)
r1.get_totals()
r1.get_date()
r1.get_phone()
print(r1)
'''
