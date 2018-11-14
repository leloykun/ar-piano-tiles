from imutils.video import VideoStream
import numpy as np
import argparse
import datetime
import imutils
import time
import cv2
import sys

WORK_DIR = "/home/leloy/Github/piano_tiles/"
MARK_THRESH = 0.20
MIN_AREA = 500

vs = VideoStream(src=0).start()
time.sleep(1.0)

def get_frame(width):
    frame = vs.read()
    frame = imutils.resize(frame, width=width)
    frame = cv2.flip(frame, 1)
    return frame

def to_gray(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    return gray

first_frame = None
text = "Unoccupied"

def read_from_file():
    with open(WORK_DIR + "finder_input.txt", 'r') as f:
        return f.readline()
def print_to_file(msg):
    with open(WORK_DIR + "finder_output.txt", 'w') as f:
        f.write(msg)

s = read_from_file()
while s not in ['break', 'quit']:
    time.sleep(0.05)

    raw_frame = get_frame(width=400)
    frame = to_gray(raw_frame)

    if first_frame is None or s == 'restart':
        first_frame = frame
        sys.stdout.write("restarted!" + '\n')
        sys.stdout.flush()
        s = read_from_file()
        continue

    frame_delta = cv2.absdiff(first_frame, frame)

    thresh = cv2.threshold(frame_delta, 50, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    res = [1 if np.sum(thresh[150:300, 100*i:100*(i+1)]) / (255*150*100) >= MARK_THRESH else 0 for i in range(4)]
    print_to_file(','.join(map(str, res)) + '\n')

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    for c in cnts:
        if cv2.contourArea(c) < MIN_AREA:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(raw_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    # draw the text and timestamp on the frame
    cv2.putText(raw_frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(raw_frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, raw_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# show the frame and record if the user presses a key
    cv2.imshow("Frame Delta", frame_delta)
    cv2.imshow("Threshold", thresh)
    cv2.imshow("Security Feed", raw_frame)
    key = cv2.waitKey(10) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("r"):
        first_frame = frame

    s = read_from_file()

vs.stop()
cv2.destroyAllWindows()
