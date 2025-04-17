#!/usr/bin/env python3
#
# This file is part of the GPM phenotyping scripts.
#
# Copyright (c) 2025 Jason Toney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""docstring goes here"""


import os
import sys
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def logistic_4pl(x, bottom, top, log_ed50, hill_slope):
    """docstring goes here"""
    return bottom + (top - bottom) / (1 + np.exp(hill_slope * (np.log(x) - log_ed50)))


def calculate_ed50(csv_file):
    """docstring goes here"""
    # Extract plate ID and isolate name
    args = os.path.splitext(csv_file)[0].split("_")
    plate = args[1].upper()
    isolate = args[2].upper()
    if "UVC" in plate:
        treatment = "UV-C"
        units = "J/m$^2$"
    else:
        treatment = "Quinoxyfen"
        units = "μg/mL"
    # Load the data
    data = pd.read_csv(csv_file)
    data = data[data["Treatment"].str.contains("Quinoxyfen|Speed|J/m2", na=False)]
    data["Concentration"] = data["Treatment"].str.extract(r"([\d\.]+)").astype(float)
    data = data.dropna(subset=["Concentration"])
    concentrations = data["Concentration"].values
    germination_rates = data["48hr %"].values
    # Fit the curve and generate ED50
    initial_guess = [
        min(germination_rates),
        max(germination_rates),
        np.log(np.median(concentrations)),
        -1,
    ]
    popt, _ = curve_fit(
        logistic_4pl, concentrations, germination_rates, p0=initial_guess, maxfev=10000
    )
    ed50 = np.exp(popt[2])
    if "UVC" in plate:
        ed50 = int(round(ed50, 0))
    else:
        ed50 = f"{ed50:.4f}"
    # Plot the DRC
    if "UVC" in plate:
        x_vals = np.linspace(min(concentrations), max(concentrations), 100)
    else:
        x_vals = np.logspace(
            np.log10(min(concentrations)), np.log10(max(concentrations)), 100
        )
    y_vals = logistic_4pl(x_vals, *popt)
    plt.figure()
    plt.scatter(concentrations, germination_rates, label="Data")
    plt.plot(x_vals, y_vals, label="Fitted Curve", color="red")
    plt.axvline(ed50, linestyle="--", color="green", label=f"ED50 = {ed50} {units}")
    if "UVC" not in plate:
        plt.xscale("log")
    plt.xlabel(f"{treatment} Concentration {units}")
    plt.ylabel("Germination Rate (%)")
    plt.legend()
    plt.title(f"{treatment} Dose-Response Curve: {isolate} - {plate}")
    plt.savefig(f"ED50_{isolate}_{plate}.png")
    plt.close()
    print(f"Estimated {treatment} ED50: {isolate}, {plate}: {ed50} {units}")


def main(csv_file):
    """docstring goes here"""
    os.chdir(f"{os.path.dirname(__file__)}/results")
    calculate_ed50(csv_file)


if __name__ == "__main__":
    main(sys.argv[1])
