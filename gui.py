#!/usr/bin/python3

"""Simple GUI wrapper for the GPM phenotyping modules"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os.path
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
        file_menu.add_command(label="Open", command=self.open_files)
        file_menu.add_command(label="Quit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)

    def create_widgets(self):
        """UI layout - columns and buttons"""
        files_frame = tk.Frame(self)
        files_frame.pack(side="top", fill="both", expand=True)

        open_label = tk.Label(files_frame, text="Open Files")
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

    def open_files(self):
        """Open csv results files"""
        self.filepaths = filedialog.askopenfilenames(
            title="Open CSV", filetypes=[("CSV files", "*.csv")]
        )
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
    app = App()
    app.mainloop()
