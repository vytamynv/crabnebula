# For Datetime Calculation
from datetime import datetime

"""
SN 1054 is recorded to be seen on 4th July 1054 by Chinese ancient civilization.
"""
BIRTHDAY = datetime.strptime("1054-07-04", "%Y-%m-%d")


"""
Manipulating the files
"""


def load_raw_data(filename):
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


def format_data(raw_data):
    """
    Arrange raw data

    Args:
        raw_data (str): raw data with noise

    Returns:
        dict: A dictionary contains the crucial cleaned data

    Raises:
        ValueError: If rawData format is invalid or cannot be parsed
    """
    brightness_mag = {}
    for dline in raw_data:
        dline = dline.split(",")
        key = dline[0]
        value = [dline[4], dline[-1]]

        if key not in brightness_mag:   # There could be repeated keys
            brightness_mag[key] = []
        brightness_mag[key].append(value)
    return brightness_mag


def write_data(filename, fData):
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


def num_day_cal(d):
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