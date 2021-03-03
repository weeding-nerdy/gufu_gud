from gufugud import parse
from gufugud import temp
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
import serial
import sys

parser = argparse.ArgumentParser(description='Plot gufu_gud data.')
parser.add_argument('path', nargs=1)
parser.add_argument('--resistance', '-r', type=float,
                    help='Cold resistance of the atomizer', required=True)
parser.add_argument('--temperature', '--temp', '-t',
                    type=float, help='Set temperature in C')
args = parser.parse_args()

path = args.path[0]
filename = os.path.splitext(path)[0]

df = pd.read_csv(path)
df = parse.parse_df(df)
df = temp.calculate_temp(df, args.resistance, 'ss316l', 'tfr')
df = parse.decimate_df(df)

max_temp = args.temperature + 30
last_timestamp = df.t[df.t.last_valid_index()]

plot = df.plot(
    y=['v', 'i', 'p'],
    x='t',
    xlim=(0, last_timestamp),
    ylim=(0, df['p'].max()),
    figsize=(32, 18),
    xlabel='Puff Time (s)',
    title='Power/Current/Voltage'
)
plt.tight_layout()
plot_path = f'power-{filename}.png'
plot.get_figure().savefig(plot_path, dpi=256)
print(f'Wrote {plot_path}')

plot = df.plot(
    y=['r'],
    x='t',
    xlim=(0, last_timestamp),
    ylim=(args.resistance - 0.2, args.resistance + 0.2),
    figsize=(32, 18),
    xlabel='Puff Time (s)',
    ylabel='Ohms',
    title='Resistance'
)
plt.tight_layout()
plot_path = f'resistance-{filename}.png'
plot.get_figure().savefig(plot_path, dpi=256)
print(f'Wrote {plot_path}')

plt.figure(figsize=(32, 18))
pp = sns.relplot(data=df, x='t_quant', y='temp', kind='line', height=16)
pp.set(xlabel='Puff Time (s)', ylabel='Temperature (C)', title='Temperature')
plt.grid(b=True)
pp.set(ylim=(0, max_temp))
pp.set(xlim=(0, last_timestamp))
if args.temperature is not None:
    plt.axhline(linewidth=2, color='r', y=args.temperature)
plt.tight_layout()
plt.savefig(f'temp-{filename}.png', dpi=256)
print(f'Wrote temp-{filename}.png')
