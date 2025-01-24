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

"""This script removes the files created by AnalyzeSporesAndGermlings.ijm."""

import os
import shutil


def cleanup_imagej():
    """Clean up any results files that exist."""
    print("Cleaning up ImageJ files...")
    os.chdir(os.path.dirname(__file__))
    imagej_path = "ImageJ/GPM"
    removed_files, removed_folders = 0, 0
    for folder in "images", "results":
        for obj in os.listdir(f"{imagej_path}/{folder}"):
            current_obj = os.path.join(f"{imagej_path}/{folder}", obj)
            if os.path.isdir(current_obj):
                print(f"Removing: {current_obj}.")
                shutil.rmtree(current_obj)
                removed_folders += 1
            elif os.path.isfile(current_obj):
                os.remove(current_obj)
                removed_files += 1
    print("Cleanup complete.")
    print(f"Deleted {removed_files} files.")
    print(f"Deleted {removed_folders} folders.")
    input("Press ENTER to exit.\n")


if __name__ == "__main__":
    cleanup_imagej()
