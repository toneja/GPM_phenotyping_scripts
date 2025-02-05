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

"""This script updates this repository with the latest version from Github."""

import io
import os
import requests
import subprocess
import zipfile


def main():
    """Download and install the update zip file."""
    # Download the zip file
    URL = "https://github.com/toneja/GPM_phenotyping_scripts/archive/refs/heads/revolution.zip"
    print(f"Downloading update package from {URL}")
    archive = requests.get(URL, timeout=5)
    # Unpack the zip file
    print("Extracting update files...")
    with zipfile.ZipFile(io.BytesIO(archive.content)) as zip_arc:
        zip_arc.extractall("../..")
    # Run the setup batch file in case of updated dependencies
    print("Updating dependencies...")
    subprocess.run(
        ["InstallDependencies.bat"],
        shell=True,
        check=True,
        text=True,
        capture_output=False,
    )
    input("File update complete. Press ENTER to close.")


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
