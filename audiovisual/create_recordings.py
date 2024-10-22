import cv2
import os
import re

IMAGE_DIR = '/Users/nicholasburczyk/Documents/Coding/FretWatch/audiovisual/content'
OUTPUT_VIDEO = 'output_video.mp4'
FPS = 30


def numerical_sort(value):
    parts = re.findall(r'\d+', value)
    return int(parts[0]) if parts else 0


def create_video_from_images(image_dir, output_video, fps):
    images = [img for img in os.listdir(image_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]

    images.sort(key=numerical_sort)

    if not images:
        print("No images found in the specified directory.")
        return

    first_image_path = os.path.join(image_dir, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for image in images:
        image_path = os.path.join(image_dir, image)
        frame = cv2.imread(image_path)

        video_writer.write(frame)

    video_writer.release()
    print(f"Video saved as '{output_video}'")


if __name__ == "__main__":
    create_video_from_images(IMAGE_DIR, OUTPUT_VIDEO, FPS)