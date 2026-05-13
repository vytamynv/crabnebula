import pandas as pd
import matplotlib as plt
import numpy as py
"""
Light Curves: Scientists plot the magnitude of a supernova over time to
determine its maximum brightness.
A 3-magnitude drop in 15 days is typical after the peak, followed by a slower
decline.

This project aims to recreate the historical "rise-and-fall" lightcurve of
a supernova -- SN1054 (crab nebula) and analyze whether it is
electron-capture supernova type

Date: May 06, 2026

Author: Vytamyn
"""

"""
Extracting the data of brightness magnitude
"""


def loadRawData(filename):
    file = open(filename, "r")
    tmp = file.readline().strip()  # Skip the header
    tmp = file.readline().strip()  # Start reading from second line
    rawData = []
    while tmp:
        rawData.append(tmp)
        tmp = file.readline().strip()
    file.close()
    return rawData


def formatData(rawData):
    brightness_mag = {}
    for dline in rawData:
        dline = dline.split(",")
        key = dline[0]
        value = [dline[3], dline[-1]]

        if key not in brightness_mag:   # There could be repeated keys
            brightness_mag[key] = []
        brightness_mag[key].append(value)
    return brightness_mag


def writeData(filename, fData):
    with open(filename, "w") as file:
        for name, mags in fData.items():
            for observation in mags:
                file.write(f"{name}\t{observation[0]}\t{observation[1]}\n")

    print(f"Data successfully saved to {filename}")







if __name__ == "__main__":
    filename = "historical_supernova_data.csv"
    rdata = loadRawData(filename)
    # print(rdata)
    fData = formatData(rdata)
    # print("m_b", fData)
    new = 'extracted_data.txt'
    writeData(new, fData)









