import itertools

import numpy as np


def train_test_split(X, test_size):
    n = len(X)
    X_copy = np.copy(X)
    np.random.shuffle(X_copy)
    split_point = int(n * test_size)
    return X_copy[:split_point], X_copy[split_point:]


def get_dataset_splits(y, n):
    dataset_indices = list(range(len(y)))
    return np.array_split(dataset_indices, n)


def get_stratified_dataset_splits(y, n):
    splits = []
    l = len(y)

    # see https://docs.scipy.org/doc/numpy/reference/generated/numpy.array_split.html
    split_sizes = l / n * np.ones(n) if (l / n).is_integer() else np.array(
        (l % n) * [l // n + 1] + (n - (l % n)) * [l // n])

    positive_indices = [i for i, label in enumerate(y) if label == 1]
    negative_indices = [i for i, label in enumerate(y) if label == 0]
    dataset_positive_indices_iterator = itertools.cycle(positive_indices)
    dataset_negative_indices_iterator = itertools.cycle(negative_indices)
    for split_index, split_size in enumerate(split_sizes):
        number_of_positive_samples_in_this_split = int(split_size // 2)
        number_of_negative_samples_in_this_split = int(split_size - number_of_positive_samples_in_this_split)
        positive_split_part_indices = itertools.islice(dataset_positive_indices_iterator,
                                                       number_of_positive_samples_in_this_split)
        negative_split_part_indices = itertools.islice(dataset_negative_indices_iterator,
                                                       number_of_negative_samples_in_this_split)
        splits.append(np.array(list(itertools.chain(positive_split_part_indices, negative_split_part_indices))))
    return splits
