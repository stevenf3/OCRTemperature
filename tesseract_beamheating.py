import cv2
import pytesseract
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

for image_file in os.listdir('.'):
    if '.png' in image_file:
        frame_no = image_file.split('_')[1]
        #print(frame_no)
        image = cv2.imread(image_file)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        roi1 = gray[225:500, 120:245]
        roi2 = gray[225:500, 240:335]
        roi3 = gray[225:500, 335:410]

        _, thresh1 = cv2.threshold(roi1, 155, 255, cv2.THRESH_BINARY)
        _, thresh2 = cv2.threshold(roi2, 155, 255, cv2.THRESH_BINARY)
        _, thresh3 = cv2.threshold(roi3, 155, 255, cv2.THRESH_BINARY)

        custom_config_dig1 = r'--psm 10 -c tessedit_char_whitelist=0123456789'
        custom_config_dig2 = r'--psm 10 -c tessedit_char_whitelist=0123456789'
        custom_config_dig3 = r'--psm 10 -c tessedit_char_whitelist=0123456789'

        text_dig1 = pytesseract.image_to_string(thresh1, config=custom_config_dig1)
        text_dig2 = pytesseract.image_to_string(thresh2, config=custom_config_dig2)
        text_dig3 = pytesseract.image_to_string(thresh3, config=custom_config_dig3)
        print(f'{frame_no}: {text_dig1} {text_dig2}')

        
        cv2.imshow('ROI 1', thresh1)
        cv2.imshow('ROI 2', thresh2)
        cv2.imshow('ROI 3', thresh3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()