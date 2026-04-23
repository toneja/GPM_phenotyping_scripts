#!/usr/bin/env python3

import os

import openpyxl
import pandas as pd


def main():
    fname = "GPMPhenotypingAssay_Workbook.xlsx"
    if os.path.exists(fname):
        workbook = openpyxl.load_workbook(fname)
    else:
        print(f"Missing workbook: {fname}")
        return
    for sname in workbook.sheetnames:
        # Only process runs from UVC plates > 12
        if (
            "UVC" not in sname
            or int(sname.split(" ")[1].split("UVC")[1].split("-")[0]) < 13
        ):
            continue
        print(f"{sname}\n")
        sheet = workbook[sname]
        df = pd.DataFrame(sheet.values)
        df.columns = df.iloc[0]
        # Calculate the mean value for each treatment
        control = df.loc[df["Treatment"] == "Control", "48hr %"].mean()
        s222nm = df.loc[df["Treatment"] == "222 nm alone", "48hr %"].mean()
        s254nm = df.loc[df["Treatment"] == "254 nm alone", "48hr %"].mean()
        combo = df.loc[df["Treatment"] == "Combination", "48hr %"].mean()
        # Print the data
        print("Means:")
        print(f"Control      = {round(control, 2)}")
        print(f"222 nm alone = {round(s222nm, 2)}")
        print(f"254 nm alone = {round(s254nm, 2)}")
        print(f"Combination  = {round(combo, 2)}")
        print("\nDeltas:")
        print(f"222 nm alone = {round(control - s222nm, 2)}")
        print(f"254 nm alone = {round(control - s254nm, 2)}")
        print(f"Combination  = {round(control - combo, 2)}")
        print("=" * 30)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
