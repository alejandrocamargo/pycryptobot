import numpy as np

def moving_average(values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma[-1]

def average(last_value, values):
    values.append(last_value)
    array = np.array(values)
    return np.mean(array)