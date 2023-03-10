#!/usr/bin/python3

import os
import tkinter as tk
from tkinter import filedialog
import analyze_results
import sklearn

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analyze Results")
        self.filepaths = []
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_files)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)

    def create_widgets(self):
        run_button = tk.Button(self, text="Run", command=self.run_analysis)
        run_button.pack(pady=10)

    def open_files(self):
        self.filepaths = filedialog.askopenfilenames(title="Open CSV", filetypes=[("CSV files", "*.csv")])

    def run_analysis(self):
        if self.filepaths:
            for filepath in self.filepaths:
                analyze_results.main(filepath)
            print("Analysis complete.")
        else:
            print("Please open at least one CSV file first.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
