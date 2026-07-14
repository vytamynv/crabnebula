# For pattern identification
import re
import numpy as np
# To control data
import data_control as dc
"""
Extracting data points for x-axis and y-axis
"""


def get_x_data(filename):
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
            delta_d = dc.num_day_cal(i)
            xP.append(delta_d)

    return xP


def get_y_data(filename):
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