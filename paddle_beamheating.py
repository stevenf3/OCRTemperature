import cv2
from paddleocr import PaddleOCR
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import re
import csv
from icecream import ic

ocr = PaddleOCR(use_angle_cls=False, lang='en')

def clean_ocr_output(text):
    # Remove all non-digit, non-dot, non-minus characters
    cleaned = re.sub(r"[^\d.-]", "", text)

    # Fix multiple dots (e.g., "31.0.9" → "310.9")
    if cleaned.count('.') > 1:
        parts = cleaned.split('.')
        cleaned = parts[0] + '.' + ''.join(parts[1:])

    if cleaned.count('.') == 0:
        cleaned = cleaned[:-1]  + '.' + cleaned[-1]

    # Try to interpret as a float
    try:
        return float(cleaned)
    except ValueError:
        return None
data_rows = []

folderpath = './Sigillino Beam Heating/EveryFrame/'

for image_file in os.listdir(folderpath):
    ic(image_file)
    if '.png' in image_file:
        print(image_file)
        frame_no = image_file.split('_')[1].split('frame')[1]
        second_no = image_file.split('_')[2].split('s.')[0]

        image = cv2.imread(folderpath+image_file)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        roi_full = gray[225:500, 120:525]

        _, thresh_full = cv2.threshold(roi_full, 155, 255, cv2.THRESH_BINARY)

        text_dig_full = ocr.ocr(roi_full, cls=False)[0][0][1][0]

        cleaned_output = clean_ocr_output(text_dig_full)
        print(f'{frame_no} full: {cleaned_output}, {second_no}')
        
        data_rows.append([frame_no, second_no, cleaned_output])

        with open('temperature_data_2.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Frame Number', 'Time (s)', 'Temperature (deg C)'])
            writer.writerows(data_rows)

