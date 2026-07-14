import data_control as dc
import data_extract as de
import plot as plt

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


def main():
    """
    Run the program

    Args:
        None (None)

    Returns:
        None
    """
    filename = "source/historical_supernova_data_E.csv"
    rdata = dc.load_raw_data(filename)
    fData = dc.format_data(rdata)

    new = 'extracted_data.txt'
    dc.write_data(new, fData)
    xP = de.get_x_data(new)
    yP = de.get_y_data(new)
    plt.plotting(xP, yP)


if __name__ == "__main__":
    main()










