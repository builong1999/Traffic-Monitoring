import numpy as np

def MeanError(y_train, y_val):
    return np.sum(np.absolute(y_train-y_val))
