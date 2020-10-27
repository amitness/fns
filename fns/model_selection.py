def train_val_size(dataset, val_ratio=0.1):
    """
    Return the train and validation data sizes based on split ratio.
    :param dataset:
    :param val_ratio: Ratio for validation dataset
    :return:
    """
    val_size = int(val_ratio * len(dataset))
    train_size = len(dataset) - val_size
    return train_size, val_size
