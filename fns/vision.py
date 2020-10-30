import json
from urllib.request import urlopen

IMAGENET_LABEL_TO_CLASS_URL = 'http://bit.ly/imagenet-labels'


def imagenet_index_to_class():
    raw_mapping = json.load(urlopen(IMAGENET_LABEL_TO_CLASS_URL))
    return {int(index): class_name for index, class_name in raw_mapping.items()}
