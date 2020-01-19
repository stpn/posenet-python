import tensorflow as tf
import cv2
import time
import argparse
import os
from posenet.posenet_factory import load_model


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--image_dir', type=str, default='./images')
parser.add_argument('--num_images', type=int, default=1000)
args = parser.parse_args()


def main():

    print('Tensorflow version: %s' % tf.__version__)
    assert tf.__version__.startswith('2.'), "Tensorflow version 2.x must be used!"

    model = 'resnet50'  # mobilenet resnet50
    stride = 32  # 8, 16, 32
    quant_bytes = 4  # float
    multiplier = 1.0  # only for mobilenet

    posenet = load_model(model, stride, quant_bytes, multiplier)

    num_images = args.num_images
    filenames = [
        f.path for f in os.scandir(args.image_dir) if f.is_file() and f.path.endswith(('.png', '.jpg'))]
    if len(filenames) > num_images:
        filenames = filenames[:num_images]

    images = {f: cv2.imread(f) for f in filenames}

    start = time.time()
    for i in range(num_images):
        image = images[filenames[i % len(filenames)]]
        posenet.estimate_multiple_poses(image)

    print('Average FPS:', num_images / (time.time() - start))


if __name__ == "__main__":
    main()
