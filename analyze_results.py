#!/usr/bin/python3

"""docstring goes here"""

import csv
import logging
import os
import sys

DEBUG = False


def analyze_results(plate, isolate):
    """docstring goes here"""
    log_level = logging.INFO
    log_format = "%(message)s"
    if DEBUG:
        log_file = "DEBUG_"
    else:
        log_file = "FinalResults_"
    log_handlers = [
        logging.FileHandler(log_file + plate + "_" + isolate + ".txt"),
        logging.StreamHandler(),
    ]
    logging.basicConfig(level=log_level, format=log_format, handlers=log_handlers)

    _0hr_results = csv_handler(plate, isolate, 0)
    _48hr_results = csv_handler(plate, isolate, 48)

    resistant, efficacious = [], []
    cntl_imgs, resistant_imgs = [], []
    cntl_area, cntl_perim, cntl_circ, cntl_feret, cntl_AR, cntl_round, cntl_solidity, cntl_convex = (
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
        if len(str(block)) == 1:
            img_prefix = "Image_000"
        else:
            img_prefix = "Image_00"
        img_name = img_prefix + str(block) + ".jpg"
        area_change = round(_48hr_results[block][0] - _0hr_results[block][0], 3)
        perim_change = round(_48hr_results[block][1] - _0hr_results[block][1], 3)
        circ_change = round(_48hr_results[block][2] - _0hr_results[block][2], 3)
        feret_change = round(_48hr_results[block][3] - _0hr_results[block][3], 3)
        AR_change = round(_48hr_results[block][4] - _0hr_results[block][4], 3)
        round_change = round(_48hr_results[block][5] - _0hr_results[block][5], 3)
        solidity_change = round(_48hr_results[block][6] - _0hr_results[block][6], 3)
        convex_change = round(_48hr_results[block][7] - _0hr_results[block][7], 3)
        if get_treatments(plate, block) == CNTL:
            cntl_imgs.append(img_name)
            cntl_area.append(area_change)
            cntl_perim.append(perim_change)
            cntl_circ.append(circ_change)
            cntl_feret.append(feret_change)
            cntl_AR.append(AR_change)
            cntl_round.append(round_change)
            cntl_solidity.append(solidity_change)
            cntl_convex.append(convex_change)
            # check for possible bad control data
            if not (
                area_change > 0
                and perim_change > 0
                and circ_change < 0
                and feret_change > 0
                and AR_change > 0
                and round_change < 0
                and solidity_change < 0
                and convex_change > 0
            ):
                logging.info(
                    "Isolate %s on plate %s has possible bad control data. Check image %s for germination.",
                    isolate.upper(),
                    plate.upper(),
                    img_name,
                )
        else:
            if (
                area_change > 0
                and perim_change > 0
                and circ_change < 0
                and feret_change > 0
                and AR_change > 0
                and round_change < 0
                and solidity_change < 0
                and convex_change > 0
            ):
                resistant.append(get_treatments(plate, block))
                resistant_imgs.append(img_name + " : " + get_treatments(plate, block))
            else:
                efficacious.append(get_treatments(plate, block))

    logging.info("Results for isolate %s from %s:", isolate.upper(), plate.upper())
    logging.info("")

    if DEBUG:
        logging.info("The following images contain the controls:")
        for item in cntl_imgs:
            logging.info("\t%s", item)
        logging.info("")
        logging.info("The average area changed in the controls by:")
        for item in cntl_area:
            logging.info("\t%s", item)
        logging.info("")
        logging.info("The average perimeter changed in the controls by:")
        for item in cntl_perim:
            logging.info("\t%s", item)
        logging.info("")
        logging.info("The average circularity changed in the controls by:")
        for item in cntl_circ:
            logging.info("\t%s", item)
        logging.info("")
        logging.info("The average feret diameter changed in the controls by:")
        for item in cntl_feret:
            logging.info("\t%s", item)
        logging.info("")
        logging.info("The average aspect ratio changed in the controls by:")
        for item in cntl_AR:
            logging.info("\t%s", item)
        logging.info("")
        logging.info("The average roundness changed in the controls by:")
        for item in cntl_round:
            logging.info("\t%s", item)
        logging.info("")
        logging.info("The average solidity changed in the controls by:")
        for item in cntl_solidity:
            logging.info("\t%s", item)
        logging.info("")
        logging.info("The average convexity changed in the controls by:")
        for item in cntl_convex:
            logging.info("\t%s", item)
        logging.info("")
    else:
        efficacious_uniq = list(set(efficacious))
        efficacious_uniq.sort()
        logging.info(
            "Isolate %s is likely NOT resistant to the following treatments:",
            isolate.upper(),
        )
        for item in efficacious_uniq:
            logging.info("\t%s : %d%% certainty", item, efficacious.count(item) / 4 * 100)
        logging.info("")
        resistant_uniq = list(set(resistant))
        resistant_uniq.sort()
        logging.info(
            "Isolate %s is likely resistant to the following treatments:",
            isolate.upper(),
        )
        for item in resistant_uniq:
            logging.info("\t%s : %d%% certainty", item, resistant.count(item) / 4 * 100)
        logging.info("")
        # logging.info("The following images contain the ineffective treatments:")
        # for item in resistant_imgs:
        #     logging.info("\t%s", item)


# handle csv datasets
def csv_handler(plate, isolate, time):
    """docstring goes here"""
    # open csv file
    with open(
        "Results_" + plate + "_" + isolate + "_" + str(time) + "hr.csv", "r"
    ) as csv_file:
        # read csv as a dict so header is skipped and value lookup is simpler
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        # slice data list => [[area_avg, perim_avg, circ_avg, feret_avg, AR_avg, round_avg, solidity_avg, convex_avg], [...]]
        slice_data = []
        # set ROI count to zero
        roi_count = 0
        # set totals to zero
        area_total, perim_total, circ_total, feret_total, AR_total, round_total, solidity_total, convex_total = (
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
                circ_total += float(row["Circ."])
                feret_total += float(row["Feret"])
                AR_total += float(row["AR"])
                round_total += float(row["Round"])
                solidity_total += float(row["Solidity"])
                convex_total += float(area_total / solidity_total)
            else:
                # once we've hit the next slice, calculate averages and store the data
                area_avg = round(area_total / roi_count, 3)
                perim_avg = round(perim_total / roi_count, 3)
                circ_avg = round(circ_total / roi_count, 3)
                feret_avg = round(feret_total / roi_count, 3)
                AR_avg = round(AR_total / roi_count, 3)
                round_avg = round(round_total / roi_count, 3)
                solidity_avg = round(solidity_total / roi_count, 3)
                convex_avg = round(convex_total / roi_count, 3)
                slice_data.append(
                    [
                        area_avg,
                        perim_avg,
                        circ_avg,
                        feret_avg,
                        AR_avg,
                        round_avg,
                        solidity_avg,
                        convex_avg,
                    ]
                )
                # move to the next slice
                slice_count += 1
                # start counts and totals with current values since we're on the first of new slice
                roi_count = 1
                area_total = int(row["Area"])
                perim_total = float(row["Perim."])
                circ_total = float(row["Circ."])
                feret_total = float(row["Feret"])
                AR_total = float(row["AR"])
                round_total = float(row["Round"])
                solidity_total = float(row["Solidity"])
                convex_total = float(area_total / solidity_total)
        # outside of the loop, calculate and store values for the last slice
        area_avg = round(area_total / roi_count, 3)
        perim_avg = round(perim_total / roi_count, 3)
        circ_avg = round(circ_total / roi_count, 3)
        feret_avg = round(feret_total / roi_count, 3)
        AR_avg = round(AR_total / roi_count, 3)
        round_avg = round(round_total / roi_count, 3)
        solidity_avg = round(solidity_total / roi_count, 3)
        convex_avg = round(convex_total / roi_count, 3)
        slice_data.append(
            [
                area_avg,
                perim_avg,
                circ_avg,
                feret_avg,
                AR_avg,
                round_avg,
                solidity_avg,
                convex_avg,
            ]
        )
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
        # Isolates: LH1, MEN8B
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
        # Isolate: DDO-ME-2
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
        # Isolate: DDO-ME-2
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
        # Isolate: GAT1
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

    analyze_results(PLATE, ISOLATE)
