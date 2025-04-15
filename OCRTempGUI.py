import numpy as np
import tkinter.filedialog as tkfd
import os
#import math
import matplotlib.colors
import tkinter as tk
import ttkbootstrap as ttk #USES TTK BOOTSTRAP INSTEAD OF NORMAL TKINTER - all commands are the same, but a more modern look based on bootstrap web dev
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import matplotlib.animation as animation
import tkinter.filedialog as tkfd
import pandas as pd
from ttkbootstrap.dialogs.dialogs import Messagebox
from tkinter.simpledialog import askinteger
from icecream import ic
from time import sleep
from icecream import ic
from datetime import datetime
from math import floor
import smtplib
from ttkbootstrap.dialogs import Messagebox
import cv2
import threading
from PIL import Image, ImageTk
from paddleocr import PaddleOCR

upadx=4 #universal x padding variable
upady=4 #universal y padding variable

class OCRDisplayReader(tk.Tk):
    def __init__(self):
        super().__init__()

        self.style = ttk.Style('darkly')
        self.style.map('TEntry', foreground=[
                        ('disabled', 'white')])
        
        self.ControlFrame = ttk.Frame(self)
        self.ControlFrame.grid(column=1, row=0, sticky='news', padx=upadx, pady=upady)

        self.ViewerFrame = ttk.Frame(self)
        self.ViewerFrame.grid(column=0, row=0, sticky='news', padx=upadx, pady=upady)

        self.img_label = ttk.Label(self.ViewerFrame)
        self.img_label.pack(expand=True, fill='both', pady=upady)

        self.slider = ttk.Scale(
            self.ViewerFrame,
            from_=0,
            to=1,
            orient='horizontal',
            command=self.OnSliderChange,
            length=600
        )
        self.slider.pack(pady=upady)


        self.videopath_basename = '.'

        self.LoadVideoButton = ttk.Button(self.ControlFrame, text='Load Video', command=self.ThreadLoadVideo)
        self.LoadVideoButton.grid(column=0, row=0, columnspan=2, sticky='news', padx=upadx, pady=upady)

        self.ViewFramesButton = ttk.Button(self.ControlFrame, text='View Frames', command=self.OpenFrameViewer)
        self.ViewFramesButton.grid(column=0, row=1, columnspan=2, sticky='news', padx=upadx, pady=upady)

        self.FrameNumberLabel = ttk.Label(self.ControlFrame, text='Frame No:')
        self.FrameNumberLabel.grid(column=0, row=2, sticky='news', padx=upadx, pady=upady)
        self.FrameNumberVar = tk.StringVar()
        self.FrameNumberVar.set('0')
        self.FrameNumber = ttk.Label(self.ControlFrame, text='N/A')
        self.FrameNumber.grid(column=1, row=2, sticky='news', padx=upadx, pady=upady)

        #-----------OCR SETTINGS-------
        self.OCRSettings = ttk.LabelFrame(self.ControlFrame, text='OCR Settings')
        self.OCRSettings.grid(column=0, row=3, columnspan=2, sticky='news', padx=upadx, pady=upady)

        self.StartOCRButton = ttk.Button(self.OCRSettings, text='Start OCR', command=self.StartOCR)
        self.StartOCRButton.grid(column=0, row=10, sticky='news', padx=upadx, pady=upady)


    def ThreadLoadVideo(self):
        self.LoadVideoButton.config(state='disabled')
        self.videopath = tkfd.askopenfilename(title='Select Video File', filetypes=[('Video Files', '*.mov;*.mp4;*.avi')])
        if not self.videopath:
            Messagebox.show_error('No file selected.')
            self.LoadVideoButton.config(state='normal')
            return
        
        self.videopath_basename = os.path.basename(self.videopath).split('.')[0]
        ic(self.videopath_basename)
        threading.Thread(target=self.LoadVideo).start()
        self.LoadVideoButton.config(state='normal')
        
        
    def LoadVideo(self):
        
        cap = cv2.VideoCapture(self.videopath)

        #fps = cap.get(cv2.CAP_PROP_FPS)

        frame_count = 0
        success, frame = cap.read()
        timestamp_str = '0.00s'

        ic(self.videopath_basename)
        if not os.path.exists(self.videopath_basename):
            os.makedirs(self.videopath_basename)
            print(f'Created folder: {self.videopath_basename}')
        else:
            print(f'Folder already exists: {self.videopath_basename}')

        while success:

            if frame_count % 1 == 0:
                print('Frame: ', frame_count)
                #roi = frame[200:400, 100:300]
                cv2.imwrite(f'./{self.videopath_basename}/frame{frame_count}_{timestamp_str}_unprocessed.png' , frame)

            time_s = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            timestamp_str = f'{time_s:.2f}s'
            success, frame = cap.read()
            print('Time: ', timestamp_str)
            print('Read a new frame: ', success)
            frame_count += 1
            ic('Working')

    def OpenFrameViewer(self):
        if not hasattr(self, 'videopath_basename'):
            Messagebox.show_error('No video has been loaded yet.')
            return

        self.frame_folder = tkfd.askdirectory(title='Select Frame Folder', initialdir='.')
        self.frame_files = sorted([
            f for f in os.listdir(self.frame_folder)
            if f.endswith('unprocessed.png')
        ])

        if not self.frame_files:
            Messagebox.show_error('No frames found.')
            return

        self.current_frame_index = 0

        self.slider.config(to=len(self.frame_files) - 1)
        self.FrameNumber.configure(text='0')

        self.UpdateDisplayedImage()

    def UpdateDisplayedImage(self):
        filepath = os.path.join(self.frame_folder, self.frame_files[self.current_frame_index])
        image = Image.open(filepath)
        image = image.resize((720, 480), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(image)
        self.img_label.config(image=self.tk_image)

    def OnSliderChange(self, value):
        self.current_frame_index = int(float(value))
        self.FrameNumber.configure(text=str(self.current_frame_index))
        self.UpdateDisplayedImage()

    def StartOCR(self):
        print('Starting OCR...')
            
if __name__ == '__main__':
    app = OCRDisplayReader()
    app.wm_title('OCR Display Reader')
    app.mainloop()


