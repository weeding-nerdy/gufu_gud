import argparse
import math
import msgpack
import numpy as np
import pandas as pd
import scipy.interpolate as interp
import scipy.signal as signal
import seaborn as sns
import serial
import sys
import tqdm

parser = argparse.ArgumentParser(description='Log gufu_gud data.')
parser.add_argument('--port', '-p', help='Serial port to communicate over')

args = parser.parse_args()

if not args.port:
  print('Port is required!')
  sys.exit(1)

# Configure Serial port with 100 ms timeout
ser = serial.Serial(args.port, timeout=0.1)

# Configure msgpack unpacker for data stream decode
unpacker = msgpack.Unpacker(raw=False)
data_list = []

try:
  while True:
    # Read some bytes in
    buf = ser.read(256)
    
    if not buf:
        # Try again later
        continue
        
    # Feed data to deserialization
    unpacker.feed(buf)
    
    try:
        # Process new objects
        for obj in unpacker:
            if not isinstance(obj, dict):
                # We only want dicts!
                print(f'rejecting: {obj}\t{chr(obj)}')
                break
            
            # Save data
            data_list.append(obj)
    except (msgpack.ExtraData, msgpack.OutOfData, msgpack.FormatError, msgpack.StackError, UnicodeDecodeError) as ex:
        # These should all be (maybe?) ok?
        print(ex)
        continue
except KeyboardInterrupt:
  print('Done capturing data')
  sys.exit(1)