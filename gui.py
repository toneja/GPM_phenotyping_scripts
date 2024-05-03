#!/usr/bin/python3
#
# This file is part of the GPM phenotyping scripts.
#
# Copyright (c) 2024 Jason Toney
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

"""Simple GUI wrapper for the GPM phenotyping modules"""

import tkinter as tk
from tkinter import messagebox
import os
import sys

import analyze_results
import compile_workbook


class App(tk.Tk):
    """GUI Application"""

    def __init__(self):
        super().__init__()
        self.title("GPM Fungicide Assay Results Analyzer")
        self.filepaths = []

        # Set window size to 50% of screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width / 2)
        window_height = int(screen_height / 2)
        self.geometry(f"{window_width}x{window_height}")

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        """File menu with 'open' and 'quit' options"""
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Quit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)

    def create_widgets(self):
        """UI layout - columns and buttons"""
        files_frame = tk.Frame(self)
        files_frame.pack(side="top", fill="both", expand=True)

        open_label = tk.Label(files_frame, text="Available Files")
        open_label.pack(side="left", padx=(10, 5))

        processed_label = tk.Label(files_frame, text="Processed Files")
        processed_label.pack(side="right", padx=(5, 10))

        open_files_listbox = tk.Listbox(files_frame)
        open_files_listbox.pack(side="left", fill="both", expand=True, padx=(10, 5))

        processed_files_listbox = tk.Listbox(files_frame)
        processed_files_listbox.pack(
            side="right", fill="both", expand=True, padx=(5, 10)
        )

        run_button = tk.Button(self, text="Process Files", command=self.run_analysis)
        run_button.pack(pady=10)

        workbook_button = tk.Button(
            self, text="Compile Workbook", command=self.make_workbook
        )
        workbook_button.pack(pady=10)

        self.open_files_listbox = open_files_listbox
        self.processed_files_listbox = processed_files_listbox

        for file in os.listdir("ImageJ/GPM/results"):
            if not (file.endswith(".csv") and file.startswith("Results_plate")):
                continue
            plate_isolate = file.split("_")[1:3]
            if os.path.exists(
                f"results/FinalResults_{plate_isolate[0]}_{plate_isolate[1]}.csv"
            ):
                print(f"Skipping: {file}, already processed.")
                continue
            file_path = os.path.join("ImageJ/GPM/results", file)
            self.filepaths.append(file_path)

        if self.filepaths:
            self.open_files_listbox.delete(0, tk.END)
            for _fp in self.filepaths:
                filename = os.path.basename(_fp)
                if "0hr" in filename:
                    self.open_files_listbox.insert(tk.END, filename)

    def run_analysis(self):
        """Execute analysis only on 0 hour files"""
        if self.filepaths:
            hr0_filepaths = [_fp for _fp in self.filepaths if "0hr" in _fp]
            if hr0_filepaths:
                for filepath in hr0_filepaths:
                    analyze_results.main(filepath)
                    filename = os.path.basename(filepath)
                    self.processed_files_listbox.insert(tk.END, filename)
                print("Analysis complete.")
                messagebox.showinfo(
                    "Analysis Complete", "Analysis is complete for all selected files."
                )
            else:
                print("No CSV files with '0hr' in their name found.")
        else:
            print("Please open at least one CSV file first.")

    def make_workbook(self):
        """Compile an Excel workbook with the results"""
        if self.processed_files_listbox.size() > 0:
            compile_workbook.main()
            print("Compiled results workbook.")
            messagebox.showinfo(
                "Workbook Compiled", "Workbook has been compiled successfully."
            )
        else:
            print("You must process csv file(s) before compiling a workbook.")


if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))
    app = App()
    app.mainloop()
