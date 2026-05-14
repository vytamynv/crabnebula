import pandas as pd
# For Plotting
import matplotlib.pyplot as plt
# For numerical data handling
import numpy as np
# For pattern identification
import re
# For Datetime Calculation
from datetime import datetime
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
SN 1054 is recorded to be seen on 4th July 1054 by Chinese ancient civilization.
"""

BIRTHDAY = datetime.strptime("1054-07-04", "%Y-%m-%d")

"""
Extracting the data of brightness magnitude
"""


def loadRawData(filename):
    """
    Load raw data

    Args:
        filename (str): File contains the information

    Returns:
        str: raw data

    Raises:
        FileNotFoundError: If the specified file does not exist
        ValueError: If the file exists but contains invalid or unreadable data
    """
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
    """
    Arrange raw data

    Args:
        rawData (str): raw data with noise

    Returns:
        dict: A dictionary contains the crucial cleaned data

    Raises:
        ValueError: If rawData format is invalid or cannot be parsed
    """
    brightness_mag = {}
    for dline in rawData:
        dline = dline.split(",")
        key = dline[0]
        value = [dline[4], dline[-1]]

        if key not in brightness_mag:   # There could be repeated keys
            brightness_mag[key] = []
        brightness_mag[key].append(value)
    return brightness_mag


def writeData(filename, fData):
    """
    Save formatted data into a file

    Args:
        filename (str): Path where the file will be saved
        fData (dict): Dictionary of information to be saved

    Returns:
        None

    Raises:
        OSError: If the file cannot be created or written
        (permissions, invalid path, etc.)
        ValueError: If fData is empty or contains invalid data types
    """
    with open(filename, "w") as file:
        for name, mags in fData.items():
            for observation in mags:
                file.write(f"{name}\t{observation[0]}\t{observation[1]}\n")

    print(f"Data successfully saved to {filename}")


"""
Clean the data
"""


def numDayCal(d):
    """
    Calculate Delta_t, the day differences from July 4, 1054

    Args:
        d (str): Date when the event was observed (format: YYYY-MM-DD)

    Returns:
        int: approximate days from July 4, 1054 (Delta_t)

    Raises:
        ValueError: If input is invalid format, has invalid values (
        e.g., month > 12),
                or cannot be parsed
    """

    d1 = datetime.strptime(d, "%Y-%m-%d")
    diff = (d1 - BIRTHDAY).days
    return diff


def getXData(filename):
    """
    Extract data points of x-axis

    Args:
        filename (str): File that contains the information for x-axis

    Returns:
        list: A list of data points for x_axis

    Raises:
        FileNotFoundError: If the specified file does not exist
        ValueError: If file content cannot be parsed into x-axis data points
    """
    xP_raw = []
    xP = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                tmp = line.split("\t")[0]
                xP_raw.append(tmp)

        for i in xP_raw:
            delta_d = numDayCal(i)
            xP.append(delta_d)

    return xP


def getYData(filename):
    """
        Extract data points of y-axis

        Args:
            filename (str): File that contains the information for x-axis

        Returns:
            list: A list of data points for x_axis

        Raises:
            FileNotFoundError: If the specified file does not exist
            ValueError: If file content cannot be parsed into y-axis data points
        """
    yP = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                tmp = line.split("\t")[-1]
                # Look for numbers
                numbers = re.findall(r'-?\d+\.?\d*', tmp)

                if numbers:
                    value = float(numbers[0])
                else:
                    value = np.nan

                yP.append(value)
    return yP


"""
Plotting Data
"""


def plotting(xP, yP):
    """
    Plotting data points

    Args:
        xP (list): A list of data points of x-axis
        yP (list): A list of data points of y-axis

    Returns:
        None

    Raises:
        ValueError: If input is invalid format
    """
    # Data sets
    xPoints = np.array(xP)
    yPoints = np.array(yP)

    # drop the 'nan'
    mask = ~np.isnan(yPoints)
    x_final = xPoints[mask]
    y_final = yPoints[mask]
    # keep 'nan' as 'ghost' points
    x_blanks = xPoints[np.isnan(yPoints)]
    plt.figure(figsize=(12, 6))

    # Plotting data points
    plt.plot(x_final, y_final, '-o', color='red',
             label='Estimated Magnitudes')

    # Plotting 'ghost' points;
    # m_v = 6.5 is known as the practical, and theoretical limit of human
    # vision under ideal, dark-sky conditions
    plt.scatter(x_blanks, [6.5]*len(x_blanks), marker='*',color='gray',
                label='Qualitative Observations')
    plt.gca().invert_yaxis()

    # Adjust x-axis ratio
    x_max = x_final[0]
    x_min = x_final[0]
    for x in x_final:
        if x > x_max:
            x_max = x + 50     # 50 is a random number to set limit
        elif x <= x_min:
            x_min = x - 50     # 50 is a random number to set limit

    plt.xlim(x_min, x_max)

    # Add chart's information
    plt.xlabel(r'Days ($\Delta t$) Relative to the July 4, 1054 Discovery')
    plt.ylabel(r'Estimated Apparent Magnitude ($m_v$)')
    plt.title('Reconstructed Historical Light Curve of SN1054 (Crab '
              'Nebula): From Early Sightings to Final Decay ')

    # Add grid
    plt.grid(True, alpha=0.3)

    # Add legends
    plt.legend()

    plt.show()


def main():
    """
    Run the program

    Args:
        None (None)

    Returns:
        None
    """
    filename = "historical_supernova_data_E.csv"
    rdata = loadRawData(filename)
    # print(rdata)
    fData = formatData(rdata)
    # print("m_b", fData)
    new = 'extracted_data.txt'
    writeData(new, fData)
    xP = getXData(new)
    # print(xP)
    # print(len(xP))
    yP = getYData(new)
    # print(yP)
    # print(len(yP))
    plotting(xP, yP)


if __name__ == "__main__":
    main()










