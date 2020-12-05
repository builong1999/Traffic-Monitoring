import numpy as np
from tensorflow.keras import backend as K

def MeanError(y_true, y_pred, ):
    return K.sqrt(K.sum(K.square(y_true - y_pred)))
