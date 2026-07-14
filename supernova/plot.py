# For Plotting
import matplotlib.pyplot as plt
# For numerical data handling
import numpy as np
import pandas as pd
"""
Plotting data
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
    plt.plot(x_final, y_final, '-o', color='red', markersize=3,
             label='Estimated Magnitudes')

    # Plotting 'ghost' points;
    # m_v = 6.5 is known as the practical, and theoretical limit of human
    # vision under ideal, dark-sky conditions
    plt.scatter(x_blanks, [6.5]*len(x_blanks), marker='*', color='blue',
                label='Qualitative Observations')

    # Invert y-axis
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

    # Add threshold of daytime visibility (naked eyes)
    # m_v = -4 (July 4, 1054)
    plt.axhline(y=-4, color='gray', linestyle='--', alpha=0.7,
               label='Daytime visibility threshold')

    # No uncertainty. Historical data only shows a range; hence, [-6,-4.5]
    plt.axhspan(ymin=-6, ymax=-4.5, xmin=0, xmax=0.02, alpha=0.3, color='pink',
               label='Peak magnitude range from historical records')

    # Add chart's information
    plt.xlabel(r'Days ($\Delta t$) Relative to the July 4, 1054 Discovery')
    plt.ylabel(r'Estimated Apparent Magnitude ($m_v$)')
    plt.title('Reconstructed Historical Light Curve of SN1054 (Crab '
              'Nebula): From Early Sightings to Final Decay ')

    # Comparing with the light curve from Moriya's model
    ecsn = pd.read_csv('source/moriya-fig-data.csv')

    # Rescale
    peak_ecsn = min(ecsn['Y'])
    peak_his = np.nanmin(yP)

    shift = peak_his - peak_ecsn

    y_aligned = []
    tmp = 0
    for i in ecsn['Y']:
        tmp = i + shift
        y_aligned.append(tmp)

    plt.plot(ecsn['X'], y_aligned, 'g--', linewidth=2,
             label='ECSN + wind model (Moriya et al. 2014)')


    # Add grid
    plt.grid(True, alpha=0.3)

    # Add legends
    plt.legend()

    plt.show()