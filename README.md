# GufuGud
## What is GufuGud?
GufuGud is Icelandic for "Vapor God". In addition it is a collection of Open Source hardware and software that allows precise measurement of vaporizer atomizer coils.

## Prerequisites
1. Install PlatformIO: https://platformio.org/platformio-ide
2. Set up a Python >= 3.7 environment with the following packages installed:
    * Jupyter Lab
    * Scipy
    * Numpy
    * Pandas
    * Matplotlib
    * Seaborn
    * PySerial
    * Msgpack
    * Tqdm

## gg_interface
GufuGud Interface is a data acquisition system for precision voltage and current measurement across/through a vaporizer atomizer. This allows both Power and Resistance to be calculated. In order to minimize the errors associated with resistance measurement, Four-Terminal Sensing (also called a Kelvin measurement) is used to measure the voltage and current across/through the atomizer: https://en.wikipedia.org/wiki/Four-terminal_sensing

The interface is comprised of a TI INA260EVM connected to a Teensy 3.6 via I2C, and is written in C++ using the Arduino platform in a PlatformIO project. The Teensy reads the voltage and current data from the INA260EVM when the ALERT line from the IC indicates that a conversion is ready. This data is then serialized into a MessagePack message, and sent to the PC via a USB virtual serial port.

Details of the interface hardware can be found in `./gg_interface/hardware/`

## gg_analyze
GufuGud Analyze is a set of Python software and tools to receive data from the GufuGud Interface, store the data for future use, and analyze the data. Algorithms are provided to preform signal processing on the raw data and convert the voltage and current data into resistance and temperature.

The analyzer connects to the USB virtual serial port provided by the GufuGud Interface, receives the MessagePack encoded data, deserializes the data, stores the data for future use, processes the data, and displays the data in graphical form.

## Licensing
* All software is licensed under the 3-Clause BSD license.
* All hardware is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).
