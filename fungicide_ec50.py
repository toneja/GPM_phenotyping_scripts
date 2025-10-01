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

"""Reads an excel datasheet and generates EC50 values for all tested fungicides."""

import os
import sys

import numpy as np
import openpyxl
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def logistic_4pl(x, bottom, top, ec50, hill_slope):
    """Logistic function for calculating EC50."""
    return bottom + (top - bottom) / (
        1 + np.exp(hill_slope * (np.log(x) - np.log(ec50)))
    )


def calculate_ec50s(file):
    """Calculate EC50's for all tested fungicides."""
    if not os.path.exists(file):
        return f"File: {file} not found."
    results_df = pd.DataFrame(
        columns=["Isolate", "Plate", "Fungicide", "EC50", "SE", "R^2", "Keep?"]
    )
    workbook = openpyxl.load_workbook(file)
    for sheet_name in workbook.sheetnames:
        # Initialize empty results
        results = pd.Series([])
        sheet = workbook[sheet_name]
        df = pd.DataFrame(sheet.values)
        df.columns = df.iloc[0]
        df = df.drop(0).reset_index(drop=True)
        if not any(x in df.columns for x in ("Treatment", "48hr %")):
            continue
        isolate = sheet_name.split(" ")[0]
        plate = sheet_name.split(" ")[1]
        fungicides = list(
            {
                f.split()[0]
                for f in df["Treatment"]
                if f.split()[0] not in {"Control", "SHAM"}
            }
        )
        fungicides.sort()
        for fungicide in fungicides:
            # ignore QOI fungicides
            if "strobin" in fungicide:
                continue
            # Extract dose and response data
            data = df.copy()
            data = data[data["Treatment"].str.contains(fungicide, na=False)]
            data["Concentration"] = (
                data["Treatment"].str.extract(r"(\d+(?:\.\d+)?)").astype(float)
                if fungicide == "Quinoxyfen"
                else data["Treatment"].str.extract(r"(\d+)").astype(int)
            )
            concentrations = data["Concentration"].values
            germination_rates = data["48hr %"].values
            # Check lower and upper bounds on germination rates
            keep = (
                "NO"
                if (
                    float(min(germination_rates)) >= 50
                    or float(max(germination_rates)) <= 50
                )
                else "YES"
            )
            # Fit the curve and generate EC50
            initial_guess = [
                min(germination_rates),
                max(germination_rates),
                np.median(concentrations),
                -1,
            ]
            bounds = (
                [0, 0, 0, -np.inf],
                [100, 100, np.inf, np.inf],
            )
            try:
                popt, pcov = curve_fit(  # pylint: disable=unbalanced-tuple-unpacking
                    logistic_4pl,
                    concentrations,
                    germination_rates,
                    p0=initial_guess,
                    maxfev=10000,
                    bounds=bounds,
                )
                ec50 = round(popt[2], 3)
                ec50_SE = np.sqrt(np.diag(pcov))[2]
                fitted = logistic_4pl(concentrations, *popt)
                r2 = round(r2_score(germination_rates, fitted), 5)
                if ec50_SE > ec50 and keep == "YES":
                    keep = "MAYBE"
                results = pd.Series(
                    [
                        isolate,
                        plate,
                        fungicide,
                        ec50,
                        ec50_SE,
                        r2,
                        keep,
                    ],
                    index=results_df.columns,
                )
                results_df = pd.concat(
                    [results_df, results.to_frame().T], ignore_index=True
                )
            except Exception as e:
                print(str(e))
        if not results.empty:
            separator = pd.Series(
                [""] * len(results_df.columns), index=results_df.columns
            )
            results_df = pd.concat(
                [results_df, separator.to_frame().T], ignore_index=True
            )
        else:
            print(f"No EC50 results available for {isolate}: {plate}")
    results_df.sort_values(by="Isolate")
    with pd.ExcelWriter("FungicideEC50s.xlsx", engine="openpyxl") as writer:
        results_df.to_excel(writer, index=False)
    return (
        results_df.to_string(index=False)
        if not results_df.empty
        else f"No EC50 results available for this workbook: {file}.\n"
    )


def main():
    """Main function. Handle any arguments."""
    os.chdir(os.path.dirname(__file__))
    results = (
        calculate_ec50s(sys.argv[1])
        if len(sys.argv) > 1
        else calculate_ec50s("GPMPhenotypingAssay_Workbook.xlsx")
    )
    input(results)


if __name__ == "__main__":
    main()
