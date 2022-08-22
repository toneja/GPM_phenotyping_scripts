#!/usr/bin/python3

"""docstring goes here"""

import csv
import logging
import os
import sys

DEBUG = True


def analyze_results(plate, isolate):
    """docstring goes here"""
    log_level = logging.INFO
    log_format = "%(message)s"
    if DEBUG:
        log_file = ("DEBUG_")
    else:
        log_file = ("FinalResults_")
    log_handlers = [
        logging.FileHandler(log_file + plate + "_" + isolate + ".txt"),
        logging.StreamHandler(),
    ]
    logging.basicConfig(level=log_level, format=log_format, handlers=log_handlers)

    _0hr_results = csv_handler(plate, isolate, 0)
    _48hr_results = csv_handler(plate, isolate, 48)

    resistant, efficacious, resistant_imgs = [], [], []
    cntl_imgs, cntl_area, cntl_perim, cntl_angle, cntl_circ, cntl_feret, cntl_feret_angle, cntl_min_feret, cntl_AR, cntl_round, cntl_solidity = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )

    for block in range(96):
        area_change = round(_48hr_results[block][0] - _0hr_results[block][0], 3)
        perim_change = round(_48hr_results[block][1] - _0hr_results[block][1], 3)
        angle_change = round(_48hr_results[block][2] - _0hr_results[block][2], 3)
        circ_change = round(_48hr_results[block][3] - _0hr_results[block][3], 3)
        feret_change = round(_48hr_results[block][4] - _0hr_results[block][4], 3)
        feret_angle_change = round(_48hr_results[block][5] - _0hr_results[block][5], 3)
        min_feret_change = round(_48hr_results[block][6] - _0hr_results[block][6], 3)
        AR_change = round(_48hr_results[block][7] - _0hr_results[block][7], 3)
        round_change = round(_48hr_results[block][8] - _0hr_results[block][8], 3)
        solidity_change = round(_48hr_results[block][9] - _0hr_results[block][9], 3)
        if get_treatments(plate, block) == CNTL:
            if len(str(block)) == 1:
                cntl_imgs.append("Image_000" + str(block) + ".jpg")
            else:
                cntl_imgs.append("Image_00" + str(block) + ".jpg")
            cntl_area.append(area_change)
            cntl_perim.append(perim_change)
            cntl_angle.append(angle_change)
            cntl_circ.append(circ_change)
            cntl_feret.append(feret_change)
            cntl_feret_angle.append(angle_change)
            cntl_min_feret.append(min_feret_change)
            cntl_AR.append(AR_change)
            cntl_round.append(round_change)
            cntl_solidity.append(solidity_change)
        else:
            if area_change > 23 and perim_change > 5 and round_change < -0.1:
                if not resistant.count(get_treatments(plate, block)):
                    resistant.append(get_treatments(plate, block))
                if len(str(block)) == 1:
                    resistant_imgs.append("Image_000" + str(block) + ".jpg")
                else:
                    resistant_imgs.append("Image_00" + str(block) + ".jpg")
            else:
                if not efficacious.count(get_treatments(plate, block)):
                    efficacious.append(get_treatments(plate, block))

    logging.info(f"Results for isolate {isolate.upper()} from {plate.upper()}:")
    logging.info("")

    if DEBUG:
        logging.info("The following images contain the controls:")
        for item in cntl_imgs:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info("The average area changed in the controls by:")
        for item in cntl_area:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info("The average perimeter changed in the controls by:")
        for item in cntl_perim:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info("The average angle changed in the controls by:")
        for item in cntl_angle:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info("The average circularity changed in the controls by:")
        for item in cntl_circ:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info("The average feret diameter changed in the controls by:")
        for item in cntl_feret:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info("The average feret angle changed in the controls by:")
        for item in cntl_feret_angle:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info("The average feret minimum changed in the controls by:")
        for item in cntl_min_feret:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info("The average aspect ratio changed in the controls by:")
        for item in cntl_AR:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info("The average roundness changed in the controls by:")
        for item in cntl_round:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info("The average solidity changed in the controls by:")
        for item in cntl_solidity:
            logging.info(f"\t{item}")
        logging.info("")
    else:
        efficacious.sort()
        logging.info(
            f"Isolate {isolate.upper()} is likely NOT resistant to the following treatments:"
        )
        for item in efficacious:
            logging.info(f"\t{item}")
        logging.info("")
        resistant.sort()
        logging.info(
            f"Isolate {isolate.upper()} is likely resistant to the following treatments:"
        )
        for item in resistant:
            logging.info(f"\t{item}")
        logging.info("")
        logging.info(f"The following images contain the ineffective treatments:")
        for item in resistant_imgs:
            logging.info(f"\t{item}")


# handle csv datasets
def csv_handler(plate, isolate, time):
    """docstring goes here"""
    # open csv file
    with open(
        "Results_" + plate + "_" + isolate + "_" + str(time) + "hr.csv", "r"
    ) as csv_file:
        # read csv as a dict so header is skipped and value lookup is simpler
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        # slice data list => [[area_avg, perim_avg, angle_avg, circ_avg, feret_avg, feret_angle_avg, min_feret_avg, AR_avg, round_avg, solidity_avg], [...]]
        slice_data = []
        # set ROI count to zero
        roi_count = 0
        # set totals to zero
        area_total, perim_total, angle_total, circ_total, feret_total, feret_angle_total, min_feret_total, AR_total, round_total, solidity_total = (
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )
        # start with Slice 1
        slice_count = 1
        # iterate over the csv values row by row
        for row in csv_reader:
            # calculate totals for each slice
            if int(row["Slice"]) == slice_count:
                roi_count += 1
                area_total += int(row["Area"])
                perim_total += float(row["Perim."])
                angle_total += float(row["Angle"])
                circ_total += float(row["Circ."])
                feret_total += float(row["Feret"])
                feret_angle_total += float(row["FeretAngle"])
                min_feret_total += float(row["MinFeret"])
                AR_total += float(row["AR"])
                round_total += float(row["Round"])
                solidity_total += float(row["Solidity"])
            else:
                # once we've hit the next slice, calculate averages and store the data
                area_avg = round(area_total / roi_count, 3)
                perim_avg = round(perim_total / roi_count, 3)
                angle_avg = round(angle_total /roi_count, 3)
                circ_avg = round(circ_total / roi_count, 3)
                feret_avg = round(feret_total / roi_count, 3)
                feret_angle_avg = round(feret_angle_total / roi_count, 3)
                min_feret_avg = round(min_feret_total / roi_count, 3)
                AR_avg = round(AR_total / roi_count, 3)
                round_avg = round(round_total / roi_count, 3)
                solidity_avg = round(solidity_total / roi_count, 3)
                slice_data.append([area_avg, perim_avg, angle_avg, circ_avg, feret_avg, feret_angle_avg, min_feret_avg, AR_avg, round_avg, solidity_avg])
                # move to the next slice
                slice_count += 1
                # start counts and totals with current values since we're on the first of new slice
                roi_count = 1
                area_total = int(row["Area"])
                perim_total = float(row["Perim."])
                angle_total = float(row["Angle"])
                circ_total = float(row["Circ."])
                feret_total = float(row["Feret"])
                feret_angle_total = float(row["FeretAngle"])
                min_feret_total = float(row["MinFeret"])
                AR_total = float(row["AR"])
                round_total = float(row["Round"])
                solidity_total = float(row["Solidity"])
        # outside of the loop, calculate and store values for the last slice
        area_avg = round(area_total / roi_count, 3)
        perim_avg = round(perim_total / roi_count, 3)
        angle_avg = round(angle_total / roi_count, 3)
        circ_avg = round(circ_total / roi_count, 3)
        feret_avg = round(feret_total / roi_count, 3)
        feret_angle_avg = round(feret_angle_total / roi_count, 3)
        min_feret_avg = round(min_feret_total / roi_count, 3)
        AR_avg = round(AR_total / roi_count, 3)
        round_avg = round(round_total / roi_count, 3)
        solidity_avg = round(solidity_total / roi_count, 3)
        slice_data.append([area_avg, perim_avg, angle_avg, circ_avg, feret_avg, feret_angle_avg, min_feret_avg, AR_avg, round_avg, solidity_avg])
        # close the csv file after we're done with it
        csv_file.close()
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
        # Isolates: LH1, MEN8B
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
        ]
    elif plate == "plate1b":
        # Isolates: LH1, MEN8B
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
        ]
    elif plate == "plate2a":
        # Isolates: SC4SY-B, MICV3
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
        ]
    elif plate == "plate2b":
        # Isolates: SC4SY-B, MICV3
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
        ]
    elif plate == "plate3a":
        # Isolate: DDO-ME-2
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
        ]
    elif plate == "plate3b":
        # Isolate: DDO-ME-2
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
        ]
    elif plate == "plate4a":
        # Isolate: GAT1
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
        ]
    elif plate == "plate4b":
        # Isolate: GAT1 (48 hr images are missing for this plate + isolate.)
        treatments = []
    elif plate == "plate5a":
        # Isolates: KRAE1B, NAPA02-T
        treatments = [
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
        ]
    elif plate == "plate5b":
        # Isolates: KRAE1B, NAPA02-T
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
        ]
    elif plate == "plate6a":
        # Isolates: R532ST190-1, NAPA05-PB
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
        ]
    elif plate == "plate6b":
        # Isolates: R532ST190-1, NAPA05-PB
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
        ]
    elif plate == "plate7a":
        # Isolates: GAT1, PFV-6A
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
        ]
    elif plate == "plate7b":
        # Isolates: GAT1, PFV-6A
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
        ]
    elif plate == "plate8a":
        # Isolates: HO2, SE-22B
        treatments = [
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
        ]
    elif plate == "plate8b":
        # Isolates: HO2, SE-22B
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
        ]
    elif plate == "plate9a":
        # Isolate: CAL3B
        treatments = [
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
        ]
    elif plate == "plate9b":
        # Isolate: CAL3B
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
        ]
    elif plate == "plate10a":
        # Isolate: MITG2
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
        ]
    elif plate == "plate10b":
        # Isolate: MITG2
        treatments = [
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
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

    analyze_results(PLATE, ISOLATE)
