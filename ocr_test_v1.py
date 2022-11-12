# text recognition
import cv2
import pytesseract

# read image
img = cv2.imread('receipt-ocr-original.jpg', 0)
# configurations
config = ('-l eng --oem 1 --psm 6')

text = pytesseract.image_to_string(img, config=config, lang='eng')

# print text
#text = text.split('\n')
print(text)