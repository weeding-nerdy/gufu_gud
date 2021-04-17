from gufugud import parse
from gufugud import temp
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

parser = argparse.ArgumentParser(description='Compare multiple puffs')
parser.add_argument('paths', nargs='*')
parser.add_argument('--resistance', '-r', type=float,
                    help='Cold resistance of the atomizer', required=True)
parser.add_argument('--temperature', '--temp', '-t',
                    type=float, help='Set temperature in C')
parser.add_argument('--material', '--mat', '-m',
                    default='ss316l', help='Material (ss316l or escc_v1)')
args = parser.parse_args()

# Ensure there are at least two paths to compare
if len(args.paths) < 2:
    raise ValueError(
        f'Must supply two or more paths! Paths given: {args.paths}')

dfs = []

for path in args.paths:
    # Load each file into a dataframe
    df = pd.read_csv(path)
    # Parse, temp-calculate, and decimate the data
    parse.parse_df(df)
    temp.calculate_temp(df, args.resistance, args.material, 'tfr')
    df = parse.decimate_df(df)
    # Get the series name for the legend
    underscore_pos = path.rfind('_')
    # Handle cases where filename is not formatted correctly
    if underscore_pos == -1:
        raise ValueError(f'{path} does not follow the format <name>_<timestamp>!')
    df['name'] = path[0:underscore_pos]
    # Add to list of dataframes
    dfs.append(df)

# Combine all dataframes together for graphing
combined_df = pd.concat(dfs)

# Graph each temp curve against each other
plt.figure(figsize=(32, 18))
pp = sns.relplot(data=combined_df, x='t_quant', y='temp',
                 hue='name', kind='line', markers=False, height=16)
plt.grid(b=True)
if args.temperature is not None:
    plt.axhline(linewidth=2, color='r', y=args.temperature)
plt.tight_layout()
plt.savefig('compare.png', dpi=256)
print('Wrote compare.png')
