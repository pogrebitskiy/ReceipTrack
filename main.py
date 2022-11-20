import cv2
import pytesseract
from Receipt import Receipt
import datetime
import re
import os


def read_receipt(filepath):
    # Read image usingVOpenCS
    img = cv2.imread(filepath, 0)
    # configurations
    config = '-l eng --oem 1 --psm 6'

    # Parse text using pytesseract
    text = pytesseract.image_to_string(img, config=config, lang='eng')

    # Create a Receipt object using the parsed text
    return Receipt(text)

if __name__ == '__main__':
    rec = read_receipt('receipts/receipt2.jpeg')
    print(rec)