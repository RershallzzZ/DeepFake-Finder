import os
from random import sample


def get_image_path(path, fn):
    fn = fn.split('.')[0]
    for _, _, files in os.walk(path):
        images = files
        images.remove(fn + '.png')
    for i in range(len(images)):
        images[i] = os.path.join(path, images[i])
    images_6 = sample(images, 6)
    return images, images_6
