import os
import torch
from models import Youtube, Bilibili, Upload, Crawler, WarningUser

BASE_WEIGHTS_PATH = os.path.join('classification', 'weights', 'face_detection', 'xception')
MODEL_FULL_PATH = os.path.join(BASE_WEIGHTS_PATH, 'all_raw.p')
MODEL_77_PATH = os.path.join(BASE_WEIGHTS_PATH, 'all_c23.p')
MODEL_60_PATH = os.path.join(BASE_WEIGHTS_PATH, 'all_c40.p')

model_full = torch.load(MODEL_FULL_PATH, map_location=lambda storage, loc: storage)
model_77 = torch.load(MODEL_77_PATH, map_location=lambda storage, loc: storage)
model_60 = torch.load(MODEL_60_PATH, map_location=lambda storage, loc: storage)

model_select = {
    'original': model_full,
    '0.77': model_77,
    '0.6': model_60
}

cuda = True

VIDEO_PATH = os.path.join("video")
IMAGE_PATH = os.path.join("image")
RESULT_PATH = os.path.join("result")
SCREENSHOT_PATH = os.path.join("screenshot")
CACHE_PATH = os.path.join('cache')

website_select = {
    'youtube': Youtube,
    'bilibili': Bilibili
}

name_2_url = {
    'youtube': 'https://www.youtube.com/',
    'bilibili': 'https://www.bilibili.com/'
}

url_2_name = {
    'https://www.youtube.com/': 'youtube',
    'https://www.bilibili.com/': 'bilibili'
}

all_website = ['youtube', 'bilibili']
