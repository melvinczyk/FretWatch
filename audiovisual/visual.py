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

def hough_top_lines(frame: np.ndarray, num_lines=12):
    edges = cv.Canny(frame, 50, 150)

    lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)
    if lines is None:
        return []

    line_len = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        line_len.append((line[0], length))

    top_lines = sorted(line_len, key=lambda x: x[1], reverse=True)[:num_lines]
    return [line[0] for line in top_lines]


def detect_strings(frame: np.ndarray, num_strings=6, angle_range=(170, 10), length_threshold=100):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 50, 150)

    cv.imshow("Edges", edges)

    lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=length_threshold, maxLineGap=10)

    if lines is None:
        print("No lines detected")
        return []

    filtered_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

        if angle_range[0] - angle_range[1] <= angle <= angle_range[0] + angle_range[1]:
            filtered_lines.append(line[0])

    if not filtered_lines:
        print("No valid lines after filtering")

    filtered_lines = sorted(filtered_lines, key=lambda line: line[1])

    grouped_lines = []
    for i in range(len(filtered_lines)):
        if i == 0:
            grouped_lines.append([filtered_lines[i]])
        else:
            last_line = grouped_lines[-1][-1]
            current_line = filtered_lines[i]
            if abs(current_line[1] - last_line[1]) < 30:
                grouped_lines[-1].append(current_line)
            else:
                grouped_lines.append([current_line])

    string_lines = [group[0] for group in grouped_lines if len(group) >= 2]

    return string_lines


def draw_lines(frame: np.ndarray, lines: np.ndarray):
    for line in lines:
        x1, y1, x2, y2 = line
        cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)


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
    scale = 127
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

        top_lines = detect_strings(frame)
        draw_lines(frame, top_lines)

        cv.rectangle(frame, (100, 100), (250, 150), (0, 0, 0), -1)
        cv.putText(frame, f'{fps} FPS', (120, 135), cv.FONT_HERSHEY_PLAIN, 2, get_fps_color(fps), 2, cv.LINE_AA)
        cv.imshow('frame', frame)

        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    camera.release()
    cv.destroyAllWindows()