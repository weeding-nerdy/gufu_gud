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
                    help='Cold resistance of the atomizer')
parser.add_argument('--temperature', '--temp', '-t',
                    type=float, help='Set temperature in C')

args = parser.parse_args()

if not args.paths or len(args.paths) < 2:
  print('Must supply two or more paths!')
  sys.exit(1)

dfs = []

for path in args.paths:
    df = pd.read_csv(path)
    parse.parse_df(df)
    temp.calculate_temp(df, args.resistance, 'ss316l', 'tfr')
    df = parse.decimate_df(df)
    underscore_pos = path.rindex('_')
    df['name'] = path[0:underscore_pos]
    dfs.append(df)

combined_df = pd.concat(dfs)

plt.figure(figsize=(32, 18))
pp = sns.relplot(data = combined_df, x='t_quant', y='temp', hue='name', kind='line', markers=False, height=16)
plt.grid(b=True)
plt.axhline(linewidth=2, color='r', y=args.temperature)
plt.tight_layout()
plt.savefig('compare.png', dpi=256)
print('Wrote compare.png')
