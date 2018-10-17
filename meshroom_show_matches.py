import os
import math
import sys
from pathlib import Path

HOME = str(Path.home())

CONFIG = {
    'INPUT_DIR': os.path.join(HOME, 't/input'),
    'CACHE_DIR': os.path.join(HOME, 't/cache')
}

CONFIG['FEATURE_EXTRACTION_DIR'] = os.path.join(CONFIG['CACHE_DIR'], 'FeatureExtraction/7b7cc75d27dd8b1c17b3ae944a06209446f23ffc')
CONFIG['FEATURE_MATCHING_DIR'] = os.path.join(CONFIG['CACHE_DIR'], 'FeatureMatching/0e87da831afb7e208ae81b829c5473095bd277d9')

CONFIG['IMAGES'] = {
    252208386: {
        'IMAGE_NAME' : os.path.join(CONFIG['INPUT_DIR'], 'IMG_1437.jpg'),
    },
    1265445039: {
        'IMAGE_NAME' : os.path.join(CONFIG['INPUT_DIR'], 'IMG_1438.jpg'),
    },
    253544879: {
        'IMAGE_NAME' : os.path.join(CONFIG['INPUT_DIR'], 'IMG_1453.jpg'),
    },
    692930789: {
        'IMAGE_NAME' : os.path.join(CONFIG['INPUT_DIR'], 'IMG_1440.jpg'),
    },
}

def matches_read(frame_a, frame_b):
    matches = {}
    with open(os.path.join(CONFIG['FEATURE_MATCHING_DIR'], '%s.matches.txt' % frame_a)) as matching_file:
        for line in matching_file:
            (_, frame_other) = [int(part) for part in line.split(' ')]
            matching_file.readline()
            num_matches = int(matching_file.readline().split(' ')[1])

            if frame_other != frame_b:
                for a in range(num_matches):
                    matching_file.readline()
                continue

            for a in range(num_matches):
                (index_a, index_b) = [int(part) for part in matching_file.readline().split(' ')]
                matches[index_a] = index_b
    return matches

def features_read(frame):
    features = []
    with open(os.path.join(CONFIG['FEATURE_EXTRACTION_DIR'], '%s.sift.feat' % frame)) as feature_file:
        for line in feature_file:
            (x, y, d, o) = [float(part) for part in line.split(' ')]
            r = d / 2
            features.append((x, y, r, o))
    return features

def image_read(frame):
    return Image.open(CONFIG['IMAGES'][frame]['IMAGE_NAME'])

frames = [252208386, 692930789]

from PIL import Image, ImageFilter, ImageDraw

green = (0, 255, 0, 255)
darkgreen = (0, 100, 0, 255)

matches = matches_read(frames[0], frames[1])

features = features_read(frames[0])
features_b = features_read(frames[1])

image = image_read(frames[0])
draw = ImageDraw.Draw(image)

for feature in range(len(features)):
    (x, y, r, o) = features[feature]

    matched = matches.get(feature, None)

    color = green if matched else darkgreen
    draw.ellipse((x - r, y - r, x + r, y + r), outline = color)
    draw.line((x, y, x + r * math.cos(o), y + r * math.sin(o)), fill = color)

    if matched:
        (x1, y1, _, _) = features_b[matched]
        draw.line((x, y, x1, y1), fill=(255, 255, 255, 255))

image.show()
