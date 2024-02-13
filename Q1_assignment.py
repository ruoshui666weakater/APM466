from BootstrapYieldCurve import BootstrapYieldCurve
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

"""Q4(a), (b), (c)"""


def get_time_to_first_coupon_payment(bond):
    """Unit is year."""
    i = 0
    while bond['BID'] != Chosen_Bonds[i]['BID']:
        i = i + 1
    """Of course, data is of 2 weeks of working days, for the second week, 2 
        more days should be counted"""
    if i > 4:
        i = i + 2
    return (30 + 29 - 8 - i) / 366


def get_number_of_payments(bond):
    """Return total number of payment of a bond"""
    a = 1
    if int(bond['MATURITY DATE'][0]) == 9:
        a += 1
    a += 2 * (int(bond['MATURITY DATE'][-1]) - 4)
    return a


def a_mysterious_boolean_function(index: int) -> bool:
    """Return true if and only if the corresponding bond is of March or Sept.
    between 2024 and 2028 inclusive.
    Note: the date is a string of form 'month/day/year', example: 3/1/2024,
          and, certainly, the year only starts with '20'. i.e. does not exist
          something like 3/1/3124 in the data to be chosen."""

    if str(df.loc[index, 'MATURITY DATE'][0]) == '3' or str(
            df.loc[index, 'MATURITY DATE'][0]) == '9':
        if int(df.loc[index, 'MATURITY DATE'][-1]) < 9 and int(
                df.loc[index, 'MATURITY DATE'][-2]) == 2:
            return True
    return False


all_yield = []  # storing yields percentages for Q5
all_forward = []  # storing forward rates for Q5

for j in range(10):  # ten days
    df = pd.read_excel('2_weeks_data.xlsx', engine='openpyxl',
                       sheet_name=j)
    yield_curve = BootstrapYieldCurve()
    # print(df.loc[1, 'YIELD'])
    Chosen_Bonds = []
    """for each day of 10, we choose 10 bonds, see below."""
    for i in range(len(df)):
        if a_mysterious_boolean_function(i):
            Chosen_Bonds.append(df.loc[i])

    for i in range(len(Chosen_Bonds)):
        yield_curve.add_data(1000, get_number_of_payments(Chosen_Bonds[i]),
                             Chosen_Bonds[i]['COUPON'],
                             Chosen_Bonds[i]['BID'],
                             get_time_to_first_coupon_payment(Chosen_Bonds[i]))

    y = yield_curve.get_spot_values()
    x = yield_curve.get_time_values()
    z = yield_curve.get_yield_values()
    # cubic_interpolation = CubicSpline(x, y)

    """4(a), 4(b), 4(c) of total 3 figures, each for loop (starts at line 49) 
        generates one curve on each figure, total of 10 curves (in each figure).
        """
    # x_new = np.linspace(0.5, 5, 1000)
    # y_new = cubic_interpolation(x_new)  #cubic spline interpolation if desired
                                          # not used in the answer.
    plt.figure(1)
    plt.plot(x, y)
    plt.title("Zero Curve")
    plt.ylabel("Zero Rate (%)")
    plt.xlabel("Maturity in Years")
    plt.xlim(1, 5)
    plt.ylim(0, 0.1)

    plt.figure(2)
    x = yield_curve.get_numbers_of_payments()
    plt.plot(x, z)
    plt.title("Yield Curve")
    plt.ylabel("Yields")
    plt.xlabel("Numbers of Coupon Payments")

    plt.figure(3)
    x = [1, 2, 3, 4, 5]
    y = yield_curve.get_forward_rates()
    plt.plot(x, y)
    plt.xlabel("Years")
    plt.ylabel("One Year Rate")
    yield_values = [item for index, item in enumerate(z) if index % 2 == 0]
    all_yield.append(yield_values)
    all_forward.append(y)
    """The plot gives a automatic linear interpolation"""
plt.show()

"""Q5: transforming random variable"""
yield_T = np.array(all_yield).T  # Treat as a matrix, take tranpose
forward_T = np.array(all_forward).T  # Treat as a matrix, take transpose
log_ratio_yield = []
log_ratio_forward = []

"""Q5, take ratio and take log for each ratio"""
for i in range(len(yield_T)):
    p = []
    for j in range(1, len(yield_T[i])):
        p.append(yield_T[i][j] / yield_T[i][j - 1])
    log_ratio_yield.append(np.log(np.array(p)))

for i in range(len(forward_T)):
    p = []
    for j in range(1, len(forward_T[i])):
        if forward_T[i][j] / forward_T[i][j - 1] <= 0:  # if one of them
            # non-positive, log value not making sense, treat such log values 0.
            p.append(1)
        else:
            p.append(forward_T[i][j] / forward_T[i][j - 1])
    log_ratio_forward.append(np.log(np.array(p)))

"""Q5: Getting covariance matrices, just using numpy builtin function."""
print(np.cov(np.array(log_ratio_yield)))
print(np.cov(np.array(log_ratio_forward)))

"""Q6: Getting eigenvalue and eigenvector, numpy builtin function."""
print(np.linalg.eig(np.cov(log_ratio_yield)))
print(np.linalg.eig(np.cov(log_ratio_forward)))
