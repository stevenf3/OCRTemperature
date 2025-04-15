import cv2
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

videopath = "./BeamHeating_10MeVCu_300deg.mov"
cap = cv2.VideoCapture(videopath)

fps = cap.get(cv2.CAP_PROP_FPS)

frame_count = 0
success, frame = cap.read()
timestamp_str = '0.00s'



while success:

    if frame_count % 1 == 0:
        print('Frame: ', frame_count)
        #roi = frame[200:400, 100:300]
        cv2.imwrite(f'unprocessed_frame{frame_count}_{timestamp_str}.png' , frame)

    time_s = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    timestamp_str = f'{time_s:.2f}s'
    success, frame = cap.read()
    print('Time: ', timestamp_str)
    print('Read a new frame: ', success)
    frame_count += 1