import numpy as np
import os
import random

BACKEND_NAME = ""
VOCAB_MODES = "standard"
N_SEEDS=1

EMBED_DATASET_DIR = ""

SIM_MARGIN = 0.1
MAX_CLUE_NUMBER = 10

_BACKEND_CACHE = {}
_VOCAB_CACHE = {}


def _l2_normalize(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def cosine_sim(a, b):
    if a is None or b is None:
        return -1.0
    return float(np.dot(a, b))