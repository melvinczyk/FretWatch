import cv2 as cv


def grab_frame(camera: cv.VideoCapture):
    if not camera.isOpened():
        print('Cannot open camera')
        exit()
    ret, frame = camera.read()
    if not ret:
        print('Cannot receive frame')
    return frame


if __name__ == '__main__':
    camera = cv.VideoCapture(0)
    while True:
        frame = grab_frame(camera)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    camera.release()
    cv.destroyAllWindows()