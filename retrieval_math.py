import math
import numpy as np


def log_frequency(tf):
    if tf:
        return 1 + np.log10(tf)
    return 0


def idf(n, df):
    return np.log10(np.true_divide(n, df))


def tf_idf(tf, n, df):
    if df:
        return np.multiply(log_frequency(tf), idf(n, df))
    return 0
