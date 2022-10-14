#!/usr/bin/python3

"""docstring goes here"""

import csv
import os
import sys
import pandas
from sklearn import linear_model
from tabulate import tabulate
from treatments import get_treatments


# debris ~ area + major + minor + circ + feret + min_feret + ar + convex + feret_ratio
# germinated ~ area + perim + min_feret + ar + solidity + convex + feret_ratio
def setup_regression(model):
    """docstring goes here"""
    df = pandas.read_csv("training_data.csv")
    if model == "Debris":
        vals = [
            "Area",
            "Major",
            "Minor",
            "Circ.",
            "Feret",
            "MinFeret",
            "AR",
            "Convex",
            "FeretRatio",
        ]
    elif model == "Germinated":
        vals = [
            "Area",
            "Perim.",
            "MinFeret",
            "AR",
            "Solidity",
            "Convex",
            "FeretRatio",
        ]
    X = df[vals]
    y = df[model]

    regression = linear_model.LogisticRegression(solver="liblinear", multi_class="ovr")
    regression.fit(X.values, y)

    return regression


def is_debris(row):
    """docstring goes here"""
    prediction = DEBRIS.predict(
        [
            [
                int(row["Area"]),
                float(row["Major"]),
                float(row["Minor"]),
                float(row["Circ."]),
                float(row["Feret"]),
                float(row["MinFeret"]),
                float(row["AR"]),
                int(row["Area"]) / float(row["Solidity"]),
                float(row["MinFeret"]) / float(row["Feret"]),
            ]
        ]
    )
    return float(prediction) >= 0.5


def is_germinated(row):
    """docstring goes here"""
    prediction = GERMINATED.predict(
        [
            [
                int(row["Area"]),
                float(row["Perim."]),
                float(row["MinFeret"]),
                float(row["AR"]),
                float(row["Solidity"]),
                int(row["Area"]) / float(row["Solidity"]),
                float(row["MinFeret"]) / float(row["Feret"]),
            ]
        ]
    )
    return float(prediction) >= 0.5


def analyze_results(plate, isolate):
    """docstring goes here"""
    _0hr_results = csv_handler(plate, isolate, 0)
    _48hr_results = csv_handler(plate, isolate, 48)

    germination_data = []
    germination_avgs = [plate, isolate]
    headers = [
        "Treatment",
        "0hr %",
        "48hr %",
        "Germinated",
        "Total",
        "Area change",
        "Perimeter change",
        "Feret change",
        "Image",
    ]
    master_headers = [
        "Plate",
        "Isol",
        "Cont",
        "Azox 10",
        "Bosc 1",
        "Bosc 10",
        "Bosc 100",
        "Dife 25",
        "Dife 250",
        "Dife 2500",
        "Fluo 1",
        "Fluo 10",
        "Fluo 100",
        "Flut 25",
        "Flut 250",
        "Flut 2500",
        "Mycl 25",
        "Mycl 250",
        "Mycl 2500",
        "Quin 0.01",
        "Quin 0.1",
        "Quin 1",
        "SHAM 100",
        "Tebu 25",
        "Tebu 250",
        "Tebu 2500",
    ]
    for block in range(96):
        if len(str(block)) == 1:
            img_prefix = "Image_000"
        else:
            img_prefix = "Image_00"
        img_name = img_prefix + str(block) + ".jpg"
        treatment = get_treatments(plate, block)
        germinated = int(_48hr_results[block][0])
        total_spores = int(_48hr_results[block][1])
        germination_0 = round(_0hr_results[block][2], 1)
        germination_48 = round(_48hr_results[block][2], 1)
        area_change = round(_48hr_results[block][3] - _0hr_results[block][3], 1)
        perim_change = round(_48hr_results[block][4] - _0hr_results[block][4], 1)
        feret_change = round(_48hr_results[block][5] - _0hr_results[block][5], 1)
        germination_data.append(
            [
                treatment,
                germination_0,
                germination_48,
                germinated,
                total_spores,
                area_change,
                perim_change,
                feret_change,
                img_name,
            ]
        )

    germination_data.sort()
    i, total = 0, 0
    for item in germination_data:
        total += item[2]
        if (i + 1) % 4 == 0:
            germination_avgs.append(round(total / 4, 1))
            total = 0
        if item[0] == "Control":
            germination_data.insert(0, germination_data.pop(i))
        i += 1

    with open(
        "FinalResults_" + plate + "_" + isolate + ".csv",
        "w",
        newline="",
    ) as csv_outfile:
        csv_writer = csv.writer(csv_outfile)
        csv_writer.writerow(headers)
        for row in germination_data:
            csv_writer.writerow(row)

    write_headers = True
    if os.path.isfile("GerminationAverages.csv"):
        write_headers = False
    with open(
        "GerminationAverages.csv",
        "a",
        newline="",
    ) as csv_outfile:
        csv_writer = csv.writer(csv_outfile)
        if write_headers:
            csv_writer.writerow(master_headers)
        csv_writer.writerow(germination_avgs)

    print(tabulate(germination_data, headers=headers))
    print(f"* Calculated results for isolate {isolate.upper()} from {plate.upper()}")
    input("Analysis complete. Press ENTER to exit.\n")


# handle csv datasets
def csv_handler(plate, isolate, time):
    """docstring goes here"""
    # open csv file
    with open(
        "Results_" + plate + "_" + isolate + "_" + str(time) + "hr.csv", "r"
    ) as csv_file:
        # read csv as a dict so header is skipped and value lookup is simpler
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        slice_data = []
        # set ROI count to zero
        roi_count, roi_germinated = 0, 0
        # set totals to zero
        area_total, perim_total, feret_total = 0, 0, 0
        # start with Slice 1
        slice_count = 1
        # iterate over the csv values row by row
        for row in csv_reader:
            # skip bad ROIs (debris)
            if is_debris(row):
                continue
            # calculate totals for each slice
            if int(row["Slice"]) == slice_count:
                roi_count += 1
                if is_germinated(row):
                    roi_germinated += 1
                area_total += int(row["Area"])
                perim_total += float(row["Perim."])
                feret_total += float(row["Feret"])
            else:
                # once we've hit the next slice, calculate percentage and store the data
                area_avg = round(area_total / roi_count, 1)
                perim_avg = round(perim_total / roi_count, 1)
                feret_avg = round(feret_total / roi_count, 1)
                slice_data.append(
                    [
                        roi_germinated,
                        roi_count,
                        roi_germinated / roi_count * 100,
                        area_avg,
                        perim_avg,
                        feret_avg,
                    ]
                )
                # move to the next slice
                slice_count += 1
                # set count to 1 since we're on the first of new slice
                roi_count = 1
                area_total = int(row["Area"])
                perim_total = float(row["Perim."])
                feret_total = float(row["Feret"])
                if is_germinated(row):
                    roi_germinated = 1
                else:
                    roi_germinated = 0
        # outside of the loop, calculate and store value for the last slice
        area_avg = round(area_total / roi_count, 1)
        perim_avg = round(perim_total / roi_count, 1)
        feret_avg = round(feret_total / roi_count, 1)
        slice_data.append(
            [
                roi_germinated,
                roi_count,
                roi_germinated / roi_count * 100,
                area_avg,
                perim_avg,
                feret_avg,
            ]
        )
        # return Slice data
        return slice_data


if __name__ == "__main__":
    if len(sys.argv) == 2:
        FN = os.path.splitext(os.path.basename(sys.argv[1]))
        ARGS = FN[0].split("_")
        PLATE = ARGS[1]
        ISOLATE = ARGS[2]
    elif len(sys.argv) == 3:
        PLATE = sys.argv[1]
        ISOLATE = sys.argv[2]
    else:
        sys.exit(f"Usage: {sys.argv[0]} [PLATE] [ISOLATE]")

    DEBRIS = setup_regression("Debris")
    GERMINATED = setup_regression("Germinated")
    analyze_results(PLATE, ISOLATE)
