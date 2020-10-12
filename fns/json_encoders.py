import json
import numpy as np


class NpEncoder(json.JSONEncoder):
    """
    Source: https://stackoverflow.com/a/57915246/10137343
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
