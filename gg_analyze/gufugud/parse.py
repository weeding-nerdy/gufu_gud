import math
import numpy as np
import pandas as pd
import scipy.signal as signal


def parse_df(df):
    # Calculate resistance and power from voltage and current
    df['r'] = df['v'] / df['i']
    df['p'] = df['v'] * df['i']

    # Quantized time to 10 Hz
    df['t_quant'] = df.t.round(1)

    # Find values where power < 0.5 Watts
    valid_mask = df.p.gt(0.5)
    for i in range(1, len(valid_mask) - 1):
        if not valid_mask[i]:
            # Also remove the last value in every series of values over 0.5 Watts since it is noisy
            # TODO: Can this be improved?
            valid_mask[i-1] = False

    # Valid data based on mask
    valid_df = df[valid_mask]

    return valid_df

def decimate_df(df):
    # Determine the start of the data
    frame_count = len(df)
    first_timestamp = df.t.iloc[0]
    print(f'Read {frame_count} frames')

    # Determine the average data rate in Hz
    data_rate = 1.0 / df['t'].diff().mean()
    print(f'Data rate is {data_rate}hz')

    # Subtract start of puff from number of seconds recorded
    puff_length = (frame_count / data_rate) - (first_timestamp * -1)
    print(f'Puff was {puff_length}s')

    # TODO: make configurable
    desired_data_rate = 100
    decimation_ratio = math.floor(data_rate / desired_data_rate)
    data_rate_multiplier = data_rate / decimation_ratio
    print(f'Decimating data by a factor of {decimation_ratio}')

    # Decimate the data to the desired data rate
    decimated_df = df[df.t.between(0, puff_length)]
    decimated_df = decimated_df.apply(lambda x: signal.decimate(
        x, decimation_ratio, ftype='fir'), axis='index')
    # t_quant needs to be re-created after decimation
    decimated_df = decimated_df.drop('t_quant', axis='columns')
    decimated_df = decimated_df.assign(t=np.arange(
        len(decimated_df)) / data_rate_multiplier)
    # Calculate quantized time (10Hz)
    decimated_df['t_quant'] = decimated_df.t.round(1)

    return decimated_df
