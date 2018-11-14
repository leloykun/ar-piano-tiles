from imutils.video import VideoStream
import numpy as np
import argparse
import datetime
import imutils
import time
import cv2
import sys

MARK_THRESH = 0.20
MIN_AREA = 500

class FootDetector:
    def __init__(self, width=400):
        self.vs = VideoStream(src=0).start()
        self.screen_width = width

        raw_frame = self.get_frame()
        gray_frame = self.to_gray(raw_frame)

        self.first_frame = gray_frame
        self.prev_frame = gray_frame
        time.sleep(1.0)

    def get_frame(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=self.screen_width)
        frame = cv2.flip(frame, 1)
        return frame

    def to_gray(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return gray

    def save(self, filename, frame):
        cv2.imwrite(filename, frame)

    def read(self, mode="first", thresh_sensitivity=50, to_save=False):
        raw_frame = self.get_frame()
        gray_frame = self.to_gray(raw_frame)
        delta_frame = cv2.absdiff(self.first_frame if mode == "first" else self.prev_frame, gray_frame)
        thresh_frame = cv2.threshold(delta_frame, thresh_sensitivity, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
        if to_save:
            self.save('latest_raw_frame.png', raw_frame)
            self.save('latest_gray_frame.png', gray_frame)
            self.save('latest_delta_frame.png', delta_frame)
            self.save('latest_thresh_frame.png', thresh_frame)
        self.prev_frame = gray_frame
        return raw_frame, gray_frame, delta_frame, thresh_frame

    def detect(self, thresh=None, mode="first", thresh_sensitivity=50):
        if thresh is None:
            _, _, _, thresh = self.read(mode, thresh_sensitivity)
        res = [1 if np.sum(thresh[150:300, 100*i:100*(i+1)]) / (255*150*100) >= MARK_THRESH else 0 for i in range(4)]
        return res;

    def show_frame(self, frame):
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):
            cv2.destroyAllWindows()
            return False
        return True
