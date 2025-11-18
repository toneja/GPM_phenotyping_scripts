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

import os
import re
import sys

import numpy as np
import openpyxl
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def logistic_4pl(x, bottom, top, ec50, hill_slope):
    """docstring goes here"""
    return bottom + (top - bottom) / (
        1 + np.exp(hill_slope * (np.log(x) - np.log(ec50)))
    )


def calculate_llda_ec50s(file):
    if not os.path.exists(file):
        return f"File: {file} not found."

    # DataFrame to store the results
    results_df = pd.DataFrame(
        columns=["Run", "Isolate", "Fungicide", "EC50", "SE", "R^2"]
    )
    workbook = openpyxl.load_workbook(file)
    for sheet_name in workbook.sheetnames:
        if not re.compile(r"^\d{2}-\d{2}$").match(sheet_name):
            continue

        sheet = workbook[sheet_name]
        data = pd.DataFrame(sheet.values)
        data.columns = data.iloc[0]
        data = data.drop(0).reset_index(drop=True)  # drop header

        isolates = data["iso"].unique()
        for isolate in isolates:
            # Extract dose and response data
            isolate_df = data[data["iso"] == isolate].copy()
            fungicides = isolate_df["fung"].unique()
            for fungicide in fungicides:
                fungicide_df = isolate_df[isolate_df["fung"] == fungicide].copy()
                # Drop missing data
                fungicide_df.dropna(subset=["pct_sev"], inplace=True)
                # Drop control data
                fungicide_df = fungicide_df[fungicide_df["conc"] != 0]
                # Get unique fungicide values and loop through them for each isolate
                concentrations = (
                    fungicide_df["conc"].values.astype(float)
                    if fungicide == "quinoxyfen"
                    else fungicide_df["conc"].values.astype(int)
                )
                germination_rates = fungicide_df["pct_sev"].values
                # This part sucks, why is there an empty list?
                if len(germination_rates) == 0:
                    print(f"Missing data: Run: {sheet_name}, Isolate: {isolate}")
                    continue
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
                    popt, pcov = curve_fit(
                        logistic_4pl,
                        concentrations,
                        germination_rates,
                        p0=initial_guess,
                        maxfev=10000,
                        bounds=bounds,
                    )
                    ec50 = round(popt[2], 5)
                    ec50_SE = np.sqrt(np.diag(pcov))[2]
                    fitted = logistic_4pl(concentrations, *popt)
                    r2 = round(r2_score(germination_rates, fitted), 5)
                    new_row = pd.Series(
                        [sheet_name, isolate, fungicide, ec50, ec50_SE, r2],
                        index=results_df.columns,
                    )
                    results_df = pd.concat(
                        [results_df, new_row.to_frame().T], ignore_index=True
                    )
                except Exception as e:
                    print(str(e))
        separator = pd.Series([""] * len(results_df.columns), index=results_df.columns)
        results_df = pd.concat([results_df, separator.to_frame().T], ignore_index=True)
    with pd.ExcelWriter(
        file, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        results_df.to_excel(writer, sheet_name="EC50 results", index=False)
    return results_df.to_string(index=False)


def main():
    os.chdir(os.path.dirname(__file__))
    results = (
        calculate_llda_ec50s(sys.argv[1])
        if len(sys.argv) > 1
        else calculate_llda_ec50s("LLDA_data_crof.xlsx")
    )
    input(results)


if __name__ == "__main__":
    main()
