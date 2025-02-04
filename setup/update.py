#!/usr/bin/env python3

import io
import os
import requests
import subprocess
import zipfile


def main():
    # Download the zip file
    URL = "https://github.com/toneja/GPM_phenotyping_scripts/archive/refs/heads/revolution.zip"
    print(f"Downloading update package from {URL}")
    archive = requests.get(URL)
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
