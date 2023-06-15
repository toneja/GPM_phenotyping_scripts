#!/usr/bin/env python3
#
# This file is part of the GPM phenotyping scripts.
#
# Copyright (c) 2023 Jason Toney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""docstring goes here"""

import os
import subprocess
import sys
import time


def batch_process(image_folder):
    """docstring goes here"""
    # Start the timer
    start_time = time.time()
    # Count how many albums are processed
    processed = 0
    # Iterate through the image folders
    for folder_name in os.listdir(image_folder):
        # Full path to the current image folder
        current_folder = os.path.join(image_folder, folder_name)

        # Check if the current item is a directory
        if os.path.isdir(current_folder):
            # rename folder to fit naming convention
            renamed_folder = "_".join(current_folder.split("_")[0:3])
            os.rename(current_folder, renamed_folder)

            # remove unnecessary extraneous files
            for file in os.listdir(renamed_folder):
                if not file.startswith("Tile0") and not file.endswith(".jpg"):
                    os.remove(f"{renamed_folder}/{file}")

            # Check if the album has already been processed
            if os.path.exists(f"GPM/images/{os.path.basename(renamed_folder)}.tif"):
                if os.path.exists(
                    f"GPM/results/Results_{os.path.basename(renamed_folder)}.csv"
                ):
                    print(f"Skipping folder: {renamed_folder}, already processed.")
                    continue
            print(f"Processing folder: {renamed_folder}")
            processed += 1

            # Execute the ImageJ macro for the current folder
            command = [
                "./ImageJ.exe",
                "-macro",
                "GPM/AnalyzeSporesAndGermlings.ijm",
                renamed_folder,
            ]

            try:
                subprocess.run(command, capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as exception:
                print(f"Error executing the macro: {exception}")

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    # Print elapsed time in H:M:S format
    print(
        f"\nElapsed time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}"
    )
    print(f"Albums processed: {processed}")
    input("Batch processing complete. Press ENTER.\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))
    if len(sys.argv) > 1:
        IMAGE_FOLDER = sys.argv[1]
    else:
        IMAGE_FOLDER = "../ECHO Images"
    batch_process(IMAGE_FOLDER)
