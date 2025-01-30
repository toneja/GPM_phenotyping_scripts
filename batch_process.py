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

"""
    This script executes the ImageJ macro and python scripts in a batch process.
    Input: all images found within the local "ECHO Images" folder.
    Output: XLSX file containing the total counts of conidia germination states.
"""


import os
import subprocess
import sys
import time
from PIL import Image

import analyze_results
import compile_workbook


def batch_process(image_folder):
    """Analyze all the images found in "ECHO Images" subdirectories."""
    # Start the timer
    start_time = time.time()
    # Count how many albums are processed
    processed = 0
    # Work inside the ImageJ directory
    os.chdir(f"{os.path.dirname(__file__)}/ImageJ")
    # Iterate through the image folders
    for folder_name in os.listdir(image_folder):
        # Full path to the current image folder
        current_folder = os.path.join(image_folder, folder_name)

        # Check if the current item is a directory
        if os.path.isdir(current_folder) and "plate" in current_folder:
            # Check if the album has already been processed
            if os.path.exists(f"GPM/images/{folder_name}") and os.path.exists(
                f"GPM/results/{folder_name}"
            ):
                print(f"Skipping folder: {current_folder}, already processed.")
                continue

            # make output folders
            os.makedirs(f"GPM/images/{folder_name}", exist_ok=True)
            os.makedirs(f"GPM/results/{folder_name}", exist_ok=True)

            print(f"Processing folder: {current_folder}")
            processed += 1

            # Convert any tif files to jpg; req for ImageJ
            for file in os.listdir(current_folder):
                file = os.path.join(current_folder, file)
                if file.endswith(".tif"):
                    with Image.open(file) as tif_file:
                        tif_file.convert("RGB").save(
                            file.replace(".tif", ".jpg"), "JPEG"
                        )

            # Execute the ImageJ macro for the current folder
            command = [
                "./ImageJ.exe",
                "-macro",
                "GPM/BatchProcess.ijm",
                current_folder,
            ]

            try:
                subprocess.run(command, capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as exception:
                print(f"Error executing the macro: {exception}")

            # Relocate output files into their respective release folders
            for file in os.listdir("GPM/images"):
                if file.endswith(".tif"):
                    os.replace(f"GPM/images/{file}", f"GPM/images/{folder_name}/{file}")
            for file in os.listdir("GPM/results"):
                if file.endswith(".csv"):
                    os.replace(
                        f"GPM/results/{file}", f"GPM/results/{folder_name}/{file}"
                    )

    # Process the ImageJ results
    for folder in os.listdir("GPM/results"):
        if folder.endswith("48hr"):
            analyze_results.main(f"ImageJ/GPM/results/{folder}")

    # Compile the results into a workbook
    compile_workbook.main()

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    # Print elapsed time in H:M:S format
    print(f"\nElapsed time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}")
    print(f"Assay runs processed: {processed // 2}")
    input("Batch processing complete. Press ENTER.\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        IMAGE_FOLDER = sys.argv[1]
    else:
        IMAGE_FOLDER = "../ECHO Images"
    batch_process(IMAGE_FOLDER)
