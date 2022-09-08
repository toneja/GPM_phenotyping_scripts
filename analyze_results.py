#!/usr/bin/python3

"""docstring goes here"""

import csv
import logging
import os
import sys
import pandas
from sklearn import linear_model
from tabulate import tabulate


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

    regression = linear_model.LogisticRegression()
    regression.fit(X, y)

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
    log_level = logging.INFO
    log_format = "%(message)s"
    log_handlers = [
        logging.FileHandler("FinalResults_" + plate + "_" + isolate + ".txt"),
        logging.StreamHandler(),
    ]
    logging.basicConfig(level=log_level, format=log_format, handlers=log_handlers)

    _0hr_results = csv_handler(plate, isolate, 0)
    _48hr_results = csv_handler(plate, isolate, 48)

    germination_data = []
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
    with open(
        "FinalResults_" + plate + "_" + isolate + ".csv",
        "w",
        newline="",
    ) as csv_outfile:
        csv_writer = csv.writer(csv_outfile)
        csv_writer.writerow(headers)
        for row in germination_data:
            csv_writer.writerow(row)

    logging.info(tabulate(germination_data, headers=headers))
    logging.info("------------------------------------------------------------")
    logging.info("* Results for isolate %s from %s", isolate.upper(), plate.upper())


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
                area_avg = round(area_total / roi_count, 3)
                perim_avg = round(perim_total / roi_count, 3)
                feret_avg = round(feret_total / roi_count, 3)
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
        area_avg = round(area_total / roi_count, 3)
        perim_avg = round(perim_total / roi_count, 3)
        feret_avg = round(feret_total / roi_count, 3)
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


# Definitions of treatments
CNTL = "Control"
SHAM = "SHAM 100 ug/mL"
AZX1 = "Azoxystrobin 10 ug/mL"
BOS1 = "Boscalid 1 ug/mL"
BOS2 = "Boscalid 10 ug/mL"
BOS3 = "Boscalid 100 ug/mL"
FLU1 = "Fluopyram 1 ug/mL"
FLU2 = "Fluopyram 10 ug/mL"
FLU3 = "Fluopyram 100 ug/mL"
MCB1 = "Myclobutanil 25 ug/mL"
MCB2 = "Myclobutanil 250 ug/mL"
MCB3 = "Myclobutanil 2500 ug/mL"
TEB1 = "Tebuconazole 25 ug/mL"
TEB2 = "Tebuconazole 250 ug/mL"
TEB3 = "Tebuconazole 2500 ug/mL"
DFC1 = "Difenoconazole 25 ug/mL"
DFC2 = "Difenoconazole 250 ug/mL"
DFC3 = "Difenoconazole 2500 ug/mL"
FTF1 = "Flutriafol 25 ug/mL"
FTF2 = "Flutriafol 250 ug/mL"
FTF3 = "Flutriafol 2500 ug/mL"
QXF1 = "Quinoxyfen 0.01 ug/mL"
QXF2 = "Quinoxyfen 0.1 ug/mL"
QXF3 = "Quinoxyfen 1 ug/mL"

# maps of treatment blocks
def get_treatments(plate, block):
    """docstring goes here"""
    if plate == "plate1a":
        # Isolates: LH1, ALV4CH-B
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            BOS1, BOS1, BOS1, BOS1,
            AZX1, AZX1, AZX1, AZX1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            MCB1, MCB1, MCB1, MCB1,
            FTF3, FTF3, FTF3, FTF3,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            TEB2, TEB2, TEB2, TEB2,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            QXF2, QXF2, QXF2, QXF2,
        ]
    elif plate == "plate1b":
        # Isolates: LH1, MEN8B, ALV4CH-B
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            CNTL, CNTL, CNTL, CNTL,
            TEB3, TEB3, TEB3, TEB3,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            FTF2, FTF2, FTF2, FTF2,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            QXF2, QXF2, QXF2, QXF2,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            DFC1, DFC1, DFC1, DFC1,
            BOS3, BOS3, BOS3, BOS3,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            MCB2, MCB2, MCB2, MCB2,
        ]
    elif plate == "plate2a":
        # Isolates: SC4SY-B, MICV3
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            MCB1, MCB1, MCB1, MCB1,
            TEB3, TEB3, TEB3, TEB3,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            QXF2, QXF2, QXF2, QXF2,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            FTF1, FTF1, FTF1, FTF1,
            BOS3, BOS3, BOS3, BOS3,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            SHAM, SHAM, SHAM, SHAM,
        ]
    elif plate == "plate2b":
        # Isolates: SC4SY-B, MICV3
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            QXF1, QXF1, QXF1, QXF1,
            TEB3, TEB3, TEB3, TEB3,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS2, BOS2, BOS2, BOS2,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            CNTL, CNTL, CNTL, CNTL,
            MCB3, MCB3, MCB3, MCB3,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            FTF2, FTF2, FTF2, FTF2,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            FLU2, FLU2, FLU2, FLU2,
        ]
    elif plate == "plate3a":
        # Isolate: DDO-ME-2, RMT2A
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            FTF1, FTF1, FTF1, FTF1,
            MCB3, MCB3, MCB3, MCB3,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            TEB2, TEB2, TEB2, TEB2,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            CNTL, CNTL, CNTL, CNTL,
            QXF3, QXF3, QXF3, QXF3,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            BOS2, BOS2, BOS2, BOS2,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            FLU2, FLU2, FLU2, FLU2,
        ]
    elif plate == "plate3b":
        # Isolate: DDO-ME-2, RMT2A
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            QXF1, QXF1, QXF1, QXF1,
            AZX1, AZX1, AZX1, AZX1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            TEB1, TEB1, TEB1, TEB1,
            BOS3, BOS3, BOS3, BOS3,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FTF2, FTF2, FTF2, FTF2,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            MCB2, MCB2, MCB2, MCB2,
        ]
    elif plate == "plate4a":
        # Isolate: GAT1, ADPN
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            FLU1, FLU1, FLU1, FLU1,
            QXF3, QXF3, QXF3, QXF3,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS2, BOS2, BOS2, BOS2,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            TEB1, TEB1, TEB1, TEB1,
            FTF3, FTF3, FTF3, FTF3,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            SHAM, SHAM, SHAM, SHAM,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            MCB2, MCB2, MCB2, MCB2,
        ]
    elif plate == "plate4b":
        # Isolate: ADPN
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            FLU1, FLU1, FLU1, FLU1,
            MCB3, MCB3, MCB3, MCB3,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            FTF2, FTF2, FTF2, FTF2,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            SHAM, SHAM, SHAM, SHAM,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            DFC1, DFC1, DFC1, DFC1,
            QXF3, QXF3, QXF3, QXF3,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            BOS2, BOS2, BOS2, BOS2,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            TEB2, TEB2, TEB2, TEB2,
        ]
    elif plate == "plate5a":
        # Isolates: KRAE1B, NAPA02-T
        treatments = [
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            QXF1, QXF1, QXF1, QXF1,
            FTF3, FTF3, FTF3, FTF3,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            TEB2, TEB2, TEB2, TEB2,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            FLU2, FLU2, FLU2, FLU2,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            CNTL, CNTL, CNTL, CNTL,
            BOS3, BOS3, BOS3, BOS3,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            MCB2, MCB2, MCB2, MCB2,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
        ]
    elif plate == "plate5b":
        # Isolates: KRAE1B, NAPA02-T
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            DFC1, DFC1, DFC1, DFC1,
            TEB3, TEB3, TEB3, TEB3,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            BOS2, BOS2, BOS2, BOS2,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            FLU1, FLU1, FLU1, FLU1,
            QXF3, QXF3, QXF3, QXF3,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB2, MCB2, MCB2, MCB2,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            SHAM, SHAM, SHAM, SHAM,
        ]
    elif plate == "plate6a":
        # Isolates: R532ST190-1, NAPA05-PB
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            FTF1, FTF1, FTF1, FTF1,
            MCB3, MCB3, MCB3, MCB3,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            TEB2, TEB2, TEB2, TEB2,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            QXF2, QXF2, QXF2, QXF2,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            DFC1, DFC1, DFC1, DFC1,
            AZX1, AZX1, AZX1, AZX1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            BOS2, BOS2, BOS2, BOS2,
        ]
    elif plate == "plate6b":
        # Isolates: R532ST190-1, NAPA05-PB
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            CNTL, CNTL, CNTL, CNTL,
            MCB3, MCB3, MCB3, MCB3,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            DFC2, DFC2, DFC2, DFC2,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            FLU1, FLU1, FLU1, FLU1,
            TEB3, TEB3, TEB3, TEB3,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS2, BOS2, BOS2, BOS2,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            QXF2, QXF2, QXF2, QXF2,
        ]
    elif plate == "plate7a":
        # Isolates: GAT1, PFV-6A
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            BOS1, BOS1, BOS1, BOS1,
            QXF3, QXF3, QXF3, QXF3,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FTF2, FTF2, FTF2, FTF2,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            MCB2, MCB2, MCB2, MCB2,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            TEB1, TEB1, TEB1, TEB1,
            DFC3, DFC3, DFC3, DFC3,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            SHAM, SHAM, SHAM, SHAM,
        ]
    elif plate == "plate7b":
        # Isolates: GAT1, PFV-6A
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            QXF1, QXF1, QXF1, QXF1,
            AZX1, AZX1, AZX1, AZX1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS2, BOS2, BOS2, BOS2,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            MCB2, MCB2, MCB2, MCB2,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            DFC1, DFC1, DFC1, DFC1,
            FLU3, FLU3, FLU3, FLU3,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            TEB2, TEB2, TEB2, TEB2,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
        ]
    elif plate == "plate8a":
        # Isolates: HO2, SE-22B
        treatments = [
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            DFC1, DFC1, DFC1, DFC1,
            BOS3, BOS3, BOS3, BOS3,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            MCB2, MCB2, MCB2, MCB2,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            TEB1, TEB1, TEB1, TEB1,
            AZX1, AZX1, AZX1, AZX1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            QXF2, QXF2, QXF2, QXF2,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
        ]
    elif plate == "plate8b":
        # Isolates: HO2, SE-22B
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            FTF1, FTF1, FTF1, FTF1,
            TEB3, TEB3, TEB3, TEB3,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            BOS2, BOS2, BOS2, BOS2,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            SHAM, SHAM, SHAM, SHAM,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            QXF1, QXF1, QXF1, QXF1,
            DFC3, DFC3, DFC3, DFC3,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            MCB2, MCB2, MCB2, MCB2,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            FLU2, FLU2, FLU2, FLU2,
        ]
    elif plate == "plate9a":
        # Isolate: CAL3B
        treatments = [
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            QXF1, QXF1, QXF1, QXF1,
            FTF3, FTF3, FTF3, FTF3,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            SHAM, SHAM, SHAM, SHAM,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            BOS2, BOS2, BOS2, BOS2,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            MCB1, MCB1, MCB1, MCB1,
            FLU3, FLU3, FLU3, FLU3,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            TEB2, TEB2, TEB2, TEB2,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
        ]
    elif plate == "plate9b":
        # Isolate: CAL3B
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            BOS1, BOS1, BOS1, BOS1,
            QXF3, QXF3, QXF3, QXF3,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            MCB2, MCB2, MCB2, MCB2,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            TEB2, TEB2, TEB2, TEB2,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            FLU1, FLU1, FLU1, FLU1,
            DFC3, DFC3, DFC3, DFC3,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            FTF2, FTF2, FTF2, FTF2,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            SHAM, SHAM, SHAM, SHAM,
        ]
    elif plate == "plate10a":
        # Isolate: MITG2
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            FTF1, FTF1, FTF1, FTF1,
            AZX1, AZX1, AZX1, AZX1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF2, QXF2, QXF2, QXF2,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            TEB2, TEB2, TEB2, TEB2,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            BOS1, BOS1, BOS1, BOS1,
            DFC3, DFC3, DFC3, DFC3,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            MCB2, MCB2, MCB2, MCB2,
        ]
    elif plate == "plate10b":
        # Isolate: MITG2
        treatments = [
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            DFC1, DFC1, DFC1, DFC1,
            FLU3, FLU3, FLU3, FLU3,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            QXF2, QXF2, QXF2, QXF2,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            TEB2, TEB2, TEB2, TEB2,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            CNTL, CNTL, CNTL, CNTL,
            BOS3, BOS3, BOS3, BOS3,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            MCB2, MCB2, MCB2, MCB2,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
        ]
    elif plate == "plate11a":
        # Isolate: BHN
        treatments = [
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            FTF1, FTF1, FTF1, FTF1,
            DFC3, DFC3, DFC3, DFC3,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF2, QXF2, QXF2, QXF2,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            MCB2, MCB2, MCB2, MCB2,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            TEB1, TEB1, TEB1, TEB1,
            AZX1, AZX1, AZX1, AZX1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            BOS2, BOS2, BOS2, BOS2,
        ]
    elif plate == "plate11b":
        # Isolate: BHN
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            BOS1, BOS1, BOS1, BOS1,
            AZX1, AZX1, AZX1, AZX1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            FTF1, FTF1, FTF1, FTF1,
            QXF3, QXF3, QXF3, QXF3,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            MCB2, MCB2, MCB2, MCB2,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            TEB2, TEB2, TEB2, TEB2,
        ]
    elif plate == "plate12a":
        # Isolate: MICV1
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            BOS1, BOS1, BOS1, BOS1,
            QXF3, QXF3, QXF3, QXF3,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            MCB2, MCB2, MCB2, MCB2,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            CNTL, CNTL, CNTL, CNTL,
            FLU3, FLU3, FLU3, FLU3,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            FTF2, FTF2, FTF2, FTF2,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            TEB2, TEB2, TEB2, TEB2,
        ]
    elif plate == "plate12b":
        # Isolate: MICV1
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            DFC1, DFC1, DFC1, DFC1,
            QXF3, QXF3, QXF3, QXF3,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            MCB2, MCB2, MCB2, MCB2,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            FLU1, FLU1, FLU1, FLU1,
            AZX1, AZX1, AZX1, AZX1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS2, BOS2, BOS2, BOS2,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            TEB2, TEB2, TEB2, TEB2,
        ]
    elif plate == "plate13a":
        # Isolate: GAT2
        treatments = [
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            CNTL, CNTL, CNTL, CNTL,
            DFC3, DFC3, DFC3, DFC3,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            FLU2, FLU2, FLU2, FLU2,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            QXF2, QXF2, QXF2, QXF2,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            BOS1, BOS1, BOS1, BOS1,
            TEB3, TEB3, TEB3, TEB3,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            MCB2, MCB2, MCB2, MCB2,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
        ]
    elif plate == "plate13b":
        # Isolate: GAT2
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            TEB1, TEB1, TEB1, TEB1,
            MCB3, MCB3, MCB3, MCB3,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            BOS2, BOS2, BOS2, BOS2,
            BOS1, BOS1, BOS1, BOS1,
            BOS3, BOS3, BOS3, BOS3,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            SHAM, SHAM, SHAM, SHAM,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            FLU1, FLU1, FLU1, FLU1,
            DFC3, DFC3, DFC3, DFC3,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            QXF2, QXF2, QXF2, QXF2,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
        ]
    elif plate == "plate14a":
        # Isolate: MICV3
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            BOS1, BOS1, BOS1, BOS1,
            MCB3, MCB3, MCB3, MCB3,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            SHAM, SHAM, SHAM, SHAM,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            FLU2, FLU2, FLU2, FLU2,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            QXF1, QXF1, QXF1, QXF1,
            FTF3, FTF3, FTF3, FTF3,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            DFC2, DFC2, DFC2, DFC2,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            TEB2, TEB2, TEB2, TEB2,
        ]
    elif plate == "plate14b":
        # Isolate: MICV3
        treatments = [
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            FLU1, FLU1, FLU1, FLU1,
            BOS3, BOS3, BOS3, BOS3,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            QXF2, QXF2, QXF2, QXF2,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            MCB1, MCB1, MCB1, MCB1,
            AZX1, AZX1, AZX1, AZX1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            TEB2, TEB2, TEB2, TEB2,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            DFC2, DFC2, DFC2, DFC2,
        ]
    elif plate == "plate15a":
        # Isolate: E1-101
        treatments = [
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            DFC1, DFC1, DFC1, DFC1,
            FLU3, FLU3, FLU3, FLU3,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            TEB2, TEB2, TEB2, TEB2,
            TEB1, TEB1, TEB1, TEB1,
            TEB3, TEB3, TEB3, TEB3,
            CNTL, CNTL, CNTL, CNTL,
            AZX1, AZX1, AZX1, AZX1,
            SHAM, SHAM, SHAM, SHAM,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            QXF1, QXF1, QXF1, QXF1,
            BOS3, BOS3, BOS3, BOS3,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            MCB2, MCB2, MCB2, MCB2,
            MCB1, MCB1, MCB1, MCB1,
            MCB3, MCB3, MCB3, MCB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
        ]
    elif plate == "plate15b":
        # Isolate: E1-101
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            TEB1, TEB1, TEB1, TEB1,
            MCB3, MCB3, MCB3, MCB3,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            QXF2, QXF2, QXF2, QXF2,
            QXF1, QXF1, QXF1, QXF1,
            QXF3, QXF3, QXF3, QXF3,
            FTF1, FTF1, FTF1, FTF1,
            FTF3, FTF3, FTF3, FTF3,
            FTF2, FTF2, FTF2, FTF2,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            BOS1, BOS1, BOS1, BOS1,
            AZX1, AZX1, AZX1, AZX1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            DFC2, DFC2, DFC2, DFC2,
            DFC1, DFC1, DFC1, DFC1,
            DFC3, DFC3, DFC3, DFC3,
            FLU1, FLU1, FLU1, FLU1,
            FLU3, FLU3, FLU3, FLU3,
            FLU2, FLU2, FLU2, FLU2,
        ]
    return treatments[block]


if __name__ == "__main__":
    if len(sys.argv) == 2:
        FN = os.path.splitext(sys.argv[1])
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
