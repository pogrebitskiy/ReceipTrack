from PIL import Image
import pytesseract
from pytesseract import Output
import numpy as np
import cv2

filename = 'receipt example.jpeg'
image = cv2.imread(filename)
results = pytesseract.image_to_data(image, output_type=Output.DICT)

text = pytesseract.image_to_string(image)
print(text)

