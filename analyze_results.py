#!/usr/bin/python3

"""docstring goes here"""

import logging
import os
import sys

from csv_handler import csv_handler
import treatments


def analyze_results(plate, isolate):
    """docstring goes here"""
    debug = True
    log_level = logging.INFO
    log_format = "%(message)s"
    log_handlers = [
        logging.FileHandler("FinalResults_" + plate + "_" + isolate + ".txt"),
        logging.StreamHandler(),
    ]
    logging.basicConfig(level=log_level, format=log_format, handlers=log_handlers)

    _0hr_results = csv_handler(plate, isolate, 0)
    _48hr_results = csv_handler(plate, isolate, 48)

    resistant, efficacious, controls_area, controls_perim, controls_roundness = (
        [],
        [],
        [],
        [],
        [],
    )

    for i in range(96):
        area_increase = round(_48hr_results[i][0] - _0hr_results[i][0], 3)
        perim_increase = round(_48hr_results[i][1] - _0hr_results[i][1], 3)
        roundness_decrease = round(_0hr_results[i][2] - _48hr_results[i][2], 3)
        if treatments.get_treatments(plate, i) == treatments.CNTL:
            controls_area.append(area_increase)
            controls_perim.append(perim_increase)
            controls_roundness.append(roundness_decrease)
        else:
            if area_increase > 23 and perim_increase > 5 and roundness_decrease > 0.1:
                if not resistant.count(treatments.get_treatments(plate, i)):
                    resistant.append(treatments.get_treatments(plate, i))
            else:
                if not efficacious.count(treatments.get_treatments(plate, i)):
                    efficacious.append(treatments.get_treatments(plate, i))

    logging.info(f"Results for isolate {isolate.upper()} from {plate.upper()}:")
    logging.info("")

    if debug:
        controls_area.sort()
        logging.info("The average area increased in the controls by:")
        for item in controls_area:
            logging.info(f"\t{item}")
        logging.info("")
        controls_perim.sort()
        logging.info("The average perimeter increased in the controls by:")
        for item in controls_perim:
            logging.info(f"\t{item}")
        logging.info("")
        controls_roundness.sort()
        logging.info("The average roundness decreased in the controls by:")
        for item in controls_roundness:
            logging.info(f"\t{item}")
        logging.info("")

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
