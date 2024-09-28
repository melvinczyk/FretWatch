import cv2 as cv
import time
import sys

import numpy as np


def grab_frame(camera: cv.VideoCapture):
    if not camera.isOpened():
        print('Cannot open camera')
        exit()
    ret, frame = camera.read()
    if not ret:
        print('Cannot receive frame')
    return frame


def threshold(frame: np.ndarray, thresh: int):
    assert (255 >= thresh >= 0)

    _, bitmap = cv.threshold(frame, thresh, 255, cv.THRESH_BINARY)
    return bitmap


def get_fps_color(fps):
    for lower, upper, color in fps_map:
        if lower <= fps <= upper:
            return color


if __name__ == '__main__':
    camera = cv.VideoCapture(0)

    new_frame_time = 0
    prev_frame_time = 0
    grey = np.zeros((1080, 1920, 3), dtype=np.uint8)
    grey[:, :, :] = [0, 255, 0]

    fps_map = [
        (0, 10, (0, 0, 255)),
        (11, 20, (0, 255, 255)),
        (21, float('inf'), (0, 255, 0))
    ]
    scale = 127  # Default threshold value
    fps = 0
    counter = 0

    while True:
        frame = grab_frame(camera)
        new_frame_time = time.time()

        if counter == 20:
            fps = 1 / (new_frame_time - prev_frame_time)
            counter = 0
        else:
            counter += 1

        prev_frame_time = new_frame_time
        fps = int(fps)

        thresh = cv.bitwise_not(frame, grey)
        blur = cv.GaussianBlur(frame, (5,5),0)
        edge = cv.Canny(frame, 50, 100)

        cv.rectangle(frame, (100, 100), (250, 150), (0, 0, 0), -1)
        cv.putText(frame, f'{fps} FPS', (120, 135), cv.FONT_HERSHEY_PLAIN, 2, get_fps_color(fps), 2, cv.LINE_AA)
        cv.imshow('frame', edge)

        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('t'):
            try:
                # Update threshold value
                scale = int(input("Enter new threshold value: "))
            except ValueError:
                print("Please enter a valid integer.")
    camera.release()
    cv.destroyAllWindows()