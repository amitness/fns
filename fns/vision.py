import json
from typing import Dict
from urllib.request import urlopen

IMAGENET_LABEL_TO_CLASS_URL = 'http://bit.ly/imagenet-labels'


def imagenet_index_to_class() -> Dict[int, str]:
    """
    Get a mapping from imagenet class index to class names.

    Returns:
        Mapping from imagenet class index to class names
    """
    raw_mapping = json.load(urlopen(IMAGENET_LABEL_TO_CLASS_URL))
    return {int(index): class_name for index, class_name in raw_mapping.items()}
