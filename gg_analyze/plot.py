import argparse
import math
import msgpack
import numpy as np
import pandas as pd
import os
import scipy.interpolate as interp
import scipy.signal as signal
import seaborn as sns
import serial
import sys
import tqdm

parser = argparse.ArgumentParser(description='Plot gufu_gud data.')
parser.add_argument('path', nargs=1)

args = parser.parse_args()

if not args.path:
  print('Path to a puff CSV is required!')
  sys.exit(1)

path = args.path[0]
df = pd.read_csv(path)
filename = os.path.splitext(path)[0]
print(f'Read {len(df)} frames')

current = df.plot(y=['v', 'i', 'p'], x='t', xlim=(0, 10))
current_path = f'current-{filename}.png'
current.get_figure().savefig(current_path)
print(f'Wrote {current_path}')

resistance = df.plot(y='r', x='t', xlim=(0, 10), ylim=(0, 10))
resistance_path = f'resistance-{filename}.png'
resistance.get_figure().savefig(resistance_path)
print(f'Wrote {resistance_path}')
