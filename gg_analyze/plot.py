from gufugud import temp
import argparse
import math
import msgpack
import numpy as np
import pandas as pd
import os
import scipy.signal as signal
import seaborn as sns
import serial
import sys
import tqdm

parser = argparse.ArgumentParser(description='Plot gufu_gud data.')
parser.add_argument('path', nargs=1)
parser.add_argument('--resistance', '-r', type=float, help='Cold resistance of the atomizer')

args = parser.parse_args()

if not args.path:
  print('Path to a CSV is required!')
  sys.exit(1)

if not args.resistance:
  print('Cold resistance is required!')
  sys.exit(1)

path = args.path[0]
df = pd.read_csv(path)
filename = os.path.splitext(path)[0]
frame_count = len(df)
print(f'Read {frame_count} frames')

data_rate = 1.0 / df['t'].diff().mean()
print(f'Data rate is {data_rate}hz')

puff_length = frame_count / data_rate
print(f'Puff was {puff_length}s')

plot = df.plot(y=['v', 'i', 'p'], x='t', xlim=(0, puff_length), ylim=(0, df['p'].max()))
plot_path = f'power-{filename}.png'
plot.get_figure().savefig(plot_path)
print(f'Wrote {plot_path}')

plot = df.plot(y=['r'], x='t', xlim=(0, puff_length), ylim=(args.resistance - 0.2, args.resistance + 0.4))
plot_path = f'resistance-{filename}.png'
plot.get_figure().savefig(plot_path)
print(f'Wrote {plot_path}')

t_func = temp.resratio_to_temp(material='ss316l', method='tfr')
df['temp'] = t_func(df.r / args.resistance)
df['temp'] = df.temp.fillna(0.0).clip(0.0, 300.0)

plot = df.plot(y=['temp'], x='t', xlim=(0, puff_length))
plot_path = f'temp-{filename}.png'
plot.get_figure().savefig(plot_path)
print(f'Wrote {plot_path}')
