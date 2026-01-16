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

"""docstring goes here."""


import os
import re
import sys
import tkinter as tk
import traceback
from io import StringIO
from tkinter import filedialog, messagebox, simpledialog, ttk

import pandas as pd

import anova_hsd
import batch_process
import calculate_ed50
import cleanup_imagej
import update


class ExcelDataEditor:
    """docstring goes here."""

    def __init__(self, root):
        """docstring goes here."""
        self.root = root
        self.root.title("Excel Data Editor - GPM Assay Data")
        self.root.geometry("1080x720")

        self.current_file = None
        self.excel_data = {}
        self.current_sheet = None
        self.text_output = None

        self.setup_ui()
        self.open_assay_workbook()

    def setup_ui(self):
        """docstring goes here."""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Add Run", command=self.add_run)
        edit_menu.add_command(label="Add Row", command=self.add_row)
        edit_menu.add_command(label="Delete Row", command=self.delete_row)
        edit_menu.add_command(label="Duplicate Row", command=self.duplicate_row)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Get Results", command=self.get_results)
        tools_menu.add_command(
            label="Plot ED50(s)", command=self.calculate_ed50_for_row
        )
        tools_menu.add_command(label="Get Stats", command=self.get_stats)
        tools_menu.add_command(label="Clean Files", command=self.cleanup_imagej)
        tools_menu.add_command(label="Update Code", command=self.update_code)

        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(toolbar, text="Open File", command=self.open_file).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(toolbar, text="Save", command=self.save_file).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(toolbar, text="Save As", command=self.save_as_file).pack(
            side=tk.LEFT, padx=(0, 10)
        )

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=(0, 10)
        )

        ttk.Button(toolbar, text="Add Run", command=self.add_run).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(toolbar, text="Add Row", command=self.add_row).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(toolbar, text="Delete Row", command=self.delete_row).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(toolbar, text="Duplicate Row", command=self.duplicate_row).pack(
            side=tk.LEFT, padx=(0, 10)
        )

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=(0, 10)
        )

        ttk.Button(toolbar, text="Get Results", command=self.get_results).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(
            toolbar, text="Plot ED50(s)", command=self.calculate_ed50_for_row
        ).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Get Stats", command=self.get_stats).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(toolbar, text="Clean Files", command=self.cleanup_imagej).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(toolbar, text="Update Code", command=self.update_code).pack(
            side=tk.LEFT, padx=(0, 5)
        )

        # Sheet selection frame
        sheet_frame = ttk.Frame(main_frame)
        sheet_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(sheet_frame, text="Sheet:").pack(side=tk.LEFT, padx=(0, 5))
        self.sheet_var = tk.StringVar()
        self.sheet_combo = ttk.Combobox(
            sheet_frame, textvariable=self.sheet_var, state="readonly", width=35
        )
        self.sheet_combo.pack(side=tk.LEFT, padx=(0, 5))
        self.sheet_combo.bind("<<ComboboxSelected>>", self.on_sheet_change)

        # Treeview frame with scrollbars
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(
            main_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        h_scrollbar.pack(fill=tk.X)
        self.tree.configure(xscrollcommand=h_scrollbar.set)

        # Right-click context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Add Row", command=self.add_row)
        self.context_menu.add_command(label="Delete Row", command=self.delete_row)
        self.context_menu.add_command(label="Duplicate Row", command=self.duplicate_row)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Archive Run(s)", command=self.archive_run)
        self.context_menu.add_command(
            label="Un-Archive Run(s)", command=self.unarchive_run
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="Plot ED50(s)", command=self.calculate_ed50_for_row
        )
        self.context_menu.add_command(label="Jump to sheet", command=self.jump_to_sheet)

        self.tree.bind("<Button-3>", self.show_context_menu)  # Right-click
        self.tree.bind("<Double-1>", self.edit_cell)  # Double-click to edit

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            main_frame, textvariable=self.status_var, relief=tk.SUNKEN
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def show_context_menu(self, event):
        """docstring goes here."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def open_file(self):
        """docstring goes here."""
        file_path = filedialog.askopenfilename(
            initialdir=".",
            title="Open Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        )

        if file_path:
            try:
                self.excel_data = pd.read_excel(file_path, sheet_name=None)
                self.current_file = file_path

                # Update sheet combo
                sheet_names = list(self.excel_data.keys())
                self.sheet_combo["values"] = sheet_names
                if sheet_names:
                    self.sheet_var.set(sheet_names[0])
                    self.current_sheet = sheet_names[0]
                    self.display_sheet()

                self.status_var.set(f"Opened: {os.path.basename(file_path)}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")

    def save_file(self):
        """docstring goes here."""
        if not self.current_file:
            self.save_as_file()
            return

        try:
            with pd.ExcelWriter(self.current_file, engine="openpyxl") as writer:
                for sheet_name, df in self.excel_data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

            self.status_var.set(f"Saved: {os.path.basename(self.current_file)}")
            messagebox.showinfo("Success", "File saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def save_as_file(self):
        """docstring goes here."""
        file_path = filedialog.asksaveasfilename(
            initialdir=".",
            title="Save Excel File",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        )

        if file_path:
            self.current_file = file_path
            self.save_file()

    def save_text_output(self):
        """docstring goes here."""
        if not self.text_output:
            messagebox.showerror("Error", "There is no text output to save.")
            return

        file_path = filedialog.asksaveasfilename(
            initialdir=".",
            title="Save Text File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_output)
            self.status_var.set(f"Saved: {os.path.basename(file_path)}")
            messagebox.showinfo("Success", "File saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def sort_by_column(self, col, reverse):
        """docstring goes here."""
        # Get all treeview data
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        # Sort Plate ID data by date string
        if col == "Plate ID":
            data.sort(
                key=lambda t: float(t[0].split("-")[2].split("hr")[0]), reverse=reverse
            )
        # Sort by ED50; ignore SE value
        elif col == "ED50 (J/m^2)":
            data.sort(
                key=lambda t: (
                    int(re.match(r"(\d+)", t[0]).group(1))
                    if not t[0] == "nan"
                    else float("inf")
                ),
                reverse=reverse,
            )
        else:
            # Try to sort numerically, fallback to string sort
            try:
                data.sort(key=lambda t: float(t[0]), reverse=reverse)
            except ValueError:
                data.sort(key=lambda t: t[0].lower(), reverse=reverse)

        # Rearrange data into sorted positions
        for index, (val, k) in enumerate(data):
            self.tree.move(k, "", index)

        # Reverse sort on next click of same header
        self.tree.heading(col, command=lambda: self.sort_by_column(col, not reverse))

    def display_sheet(self):
        """docstring goes here."""
        if not self.current_sheet or self.current_sheet not in self.excel_data:
            return

        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        df = self.excel_data[self.current_sheet]

        # Configure columns (without index)
        columns = list(df.columns)
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(
                col, text=col, command=lambda c=col: self.sort_by_column(c, False)
            )
            self.tree.column(
                col,
                width=120,
                minwidth=80,
                stretch=not any(x in col for x in ("Plate ID", "Quality Check", "Notes")),
            )

        # Insert data (without index)
        for idx, row in df.iterrows():
            values = list(row)
            # Store the actual dataframe index as a tag for internal use
            self.tree.insert("", "end", values=values, tags=(str(idx),))

    def on_sheet_change(self, _=None):
        """docstring goes here."""
        self.current_sheet = self.sheet_var.get()
        self.display_sheet()

    def get_selected_row_indices(self):
        """docstring goes here."""
        tags = []
        selections = self.tree.selection()
        if selections:
            for item in list(selections):
                tags.append(int(self.tree.item(item, "tags")[0]))
        return tags

    def add_run(self):
        """docstring goes here."""
        if not self.current_sheet == "Assay Data":
            messagebox.showwarning(
                "Warning",
                "This operation is only available when editing the 'Assay Data' sheet.",
            )
            return

        # Get path to the image directory
        folder_path = filedialog.askdirectory(
            initialdir="./ECHO Images", title="Select an Image Folder"
        )
        if not folder_path:
            return
        folder_path = os.path.basename(folder_path)

        # Sanity-check the parts of the assay folder name
        if not re.compile(
            r"^plateUVC(?P<plate>[1-9]|1[0-2])-"
            r"(?P<date>\d{6})-"
            r"(?P<timepoint>(\d+(?:\.\d+)?))hr-"
            r"(?P<wavelength>-?\d+)"
        ).match(folder_path):
            messagebox.showerror(
                "Error",
                f"Incorrect formatting of folder name: {folder_path}",
            )
            messagebox.showwarning(
                "Proper example folder name format:",
                "plateUVC12-MMDDYY-24hr-254_ISOLATE_48hr",
            )
            return

        # Extract data from directory name
        parts = folder_path.split("_")
        isolate = parts[1]
        plate = parts[0].split("plate")[1]

        # Wavelength: (irradiance, lamp length)
        lamp_dict = {254: (20.6385, 385)}
        wavelength = int(plate.split("-")[-1])
        irradiance, lamp_len = lamp_dict[wavelength][0], lamp_dict[wavelength][1]

        # Create new row with the data
        df = self.excel_data[self.current_sheet]
        new_data = [isolate, plate, "nan", "nan", irradiance, lamp_len]
        # Fill in timings from previous row if users wants
        if messagebox.askyesno(
            "Copy timing data",
            "Do you want to copy the timing data from the previous row?",
        ):
            # Get timing data from previous row
            time_cols = df.filter(like="Time").columns
            time_vals = df[time_cols].iloc[-1].tolist()
        else:
            # Fill missing timing data with nans
            time_vals = ["nan"] * (len(df.columns) - len(new_data))
        new_data.extend(time_vals)
        new_row = pd.Series(new_data, index=df.columns)

        # Add to dataframe
        self.excel_data[self.current_sheet] = pd.concat(
            [df, new_row.to_frame().T], ignore_index=True
        )

        self.display_sheet()
        self.status_var.set("New assay run added")

    def add_row(self):
        """docstring goes here."""
        if not self.current_sheet == "Assay Data":
            messagebox.showwarning(
                "Warning",
                "This operation is only available when editing the 'Assay Data' sheet.",
            )
            return

        df = self.excel_data[self.current_sheet]

        # Create new row with empty values
        new_row = pd.Series([None] * len(df.columns), index=df.columns)

        # Add to dataframe
        self.excel_data[self.current_sheet] = pd.concat(
            [df, new_row.to_frame().T], ignore_index=True
        )

        self.display_sheet()
        self.status_var.set("Row added")

    def delete_row(self):
        """docstring goes here."""
        if not self.current_sheet == "Assay Data":
            messagebox.showwarning(
                "Warning",
                "This operation is only available when editing the 'Assay Data' sheet.",
            )
            return

        row_indices = self.get_selected_row_indices()
        if row_indices is None:
            messagebox.showwarning("Warning", "No row(s) selected")
            return

        # Confirm deletion
        if messagebox.askyesno("Confirm", f"Delete row(s) {row_indices}?"):
            df = self.excel_data[self.current_sheet]
            self.excel_data[self.current_sheet] = df.drop(
                df.index[row_indices]
            ).reset_index(drop=True)

            self.display_sheet()
            self.status_var.set(f"Row(s) {row_indices} deleted")

    def duplicate_row(self):
        """docstring goes here."""
        if not self.current_sheet == "Assay Data":
            messagebox.showwarning(
                "Warning",
                "This operation is only available when editing the 'Assay Data' sheet.",
            )
            return

        row_indices = self.get_selected_row_indices()
        if row_indices is None:
            messagebox.showwarning("Warning", "No row(s) selected")
            return

        df = self.excel_data[self.current_sheet]
        self.excel_data[self.current_sheet] = pd.concat(
            [df, df.iloc[row_indices]], ignore_index=True
        )

        self.display_sheet()
        self.status_var.set(f"Row(s) {row_indices} duplicated")

    def archive_run(self):
        """docstring goes here."""
        if not self.current_sheet == "Assay Data":
            messagebox.showwarning(
                "Warning",
                "This operation is only available when editing the 'Assay Data' sheet.",
            )
            return

        row_indices = self.get_selected_row_indices()
        if row_indices is None:
            messagebox.showwarning("Warning", "No row(s) selected")
            return

        df = self.excel_data[self.current_sheet]
        archive_df = self.excel_data.get("Archived Runs")
        if archive_df is None:
            archive_df = pd.DataFrame(columns=df.columns)
            archive_df = archive_df.astype(df.dtypes.to_dict())
        # Insert archived row
        self.excel_data["Archived Runs"] = pd.concat(
            [archive_df, df.iloc[row_indices]], ignore_index=True
        )
        # Remove row from Assay Data sheet
        self.excel_data["Assay Data"] = df.drop(df.index[row_indices]).reset_index(
            drop=True
        )

        self.display_sheet()
        self.status_var.set(f"Row(s) {row_indices} archived")

    def unarchive_run(self):
        """docstring goes here."""
        if not self.current_sheet == "Archived Runs":
            messagebox.showwarning(
                "Warning",
                "This operation is only available when editing the 'Archived Runs' sheet.",
            )
            return

        row_indices = self.get_selected_row_indices()
        if row_indices is None:
            messagebox.showwarning("Warning", "No row(s) selected")
            return

        df = self.excel_data[self.current_sheet]
        assay_df = self.excel_data.get("Assay Data")
        if assay_df is None:
            # this isn't really ever going to happen, but we'll prep for it
            assay_df = pd.DataFrame(columns=df.columns)
            assay_df = assay_df.astype(df.types_to_dict())
        # Insert Un-Archived row
        self.excel_data["Assay Data"] = pd.concat(
            [assay_df, df.iloc[row_indices]], ignore_index=True
        )
        # Remove row from Archived Runs sheet
        self.excel_data["Archived Runs"] = df.drop(df.index[row_indices]).reset_index(
            drop=True
        )

        self.display_sheet()
        self.status_var.set(f"Row(s) {row_indices} un-archived")

    def edit_cell(self, event):
        """docstring goes here."""
        if not any(x in self.current_sheet for x in ("Assay Data", "Archived Runs")):
            messagebox.showwarning(
                "Warning",
                "This operation is only available when editing the 'Assay Data' or 'Archived Runs' sheets.",
            )
            return

        item = self.tree.selection()[0] if self.tree.selection() else None
        if not item:
            return

        column = self.tree.identify_column(event.x)
        col_index = int(column.replace("#", "")) - 1  # No index column offset needed
        row_index = self.get_selected_row_indices()[0]

        if row_index is None:
            return

        df = self.excel_data[self.current_sheet]
        current_value = df.iloc[row_index, col_index]

        new_value = simpledialog.askstring(
            "Edit Cell",
            "Enter new value:",
            initialvalue=str(current_value) if pd.notna(current_value) else "",
        )

        if new_value is not None:
            if new_value.isdigit():
                new_value = int(new_value)
            elif new_value.replace(".", "").isdigit():
                new_value = float(new_value)

            self.excel_data[self.current_sheet].iloc[row_index, col_index] = new_value
            self.display_sheet()
            self.status_var.set("Cell updated")

    def jump_to_sheet(self):
        """Jump to a specific sheet in the workbook"""
        if not any(x in self.current_sheet for x in ("Assay Data", "Archived Runs")):
            messagebox.showwarning(
                "Warning",
                "This operation is only available when editing the 'Assay Data' or 'Archived Runs' sheets.",
            )
            return

        row_index = self.get_selected_row_indices()
        if row_index is None:
            messagebox.showwarning("Warning", "No row selected")
            return
        if len(row_index) > 1:
            messagebox.showwarning("Warning", "You can only select 1 assay run")
            return

        df = self.excel_data[self.current_sheet]
        isolate = df.iloc[row_index]["Isolate"].item()
        plate = df.iloc[row_index]["Plate ID"].item()
        sheet_name = f"{isolate} {plate}".upper()
        if sheet_name not in list(self.excel_data.keys()):
            messagebox.showwarning("Warning", f"Sheet: {sheet_name} is not in the workbook")
            return

        self.current_sheet = sheet_name
        self.sheet_var.set(sheet_name)
        self.display_sheet()
        self.status_var.set(f"Displaying sheet {self.current_sheet}")

    def get_results(self):
        """Run batch_process.batch_process() and capture output"""
        self._run_specific_module("batch_process", "batch_process.batch_process()")

    def get_stats(self):
        """Run anova_hsd.main() and capture output"""
        self._run_specific_module("anova_hsd", "anova_hsd.main()")

    def cleanup_imagej(self):
        """Run cleanup_imagej.cleanup_imagej() and capture output"""
        self._run_specific_module("cleanup_imagej", "cleanup_imagej.cleanup_imagej()")

    def calculate_ed50_for_row(self):
        """Run calculate_ed50.main() and capture output"""
        self._run_specific_module("calculate_ed50", "calculate_ed50.main()")

    def update_code(self):
        """Run update.main() and capture output"""
        self._run_specific_module("update", "update.main()")

    def _run_specific_module(self, module_name, function_call):
        """Generic method to run a specific module's main function"""
        self.text_output = None
        # Run the module
        try:
            # Capture stdout/stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr

            stdout_capture = StringIO()
            stderr_capture = StringIO()

            # Create output window
            output_window = tk.Toplevel(self.root)
            output_window.withdraw()
            output_window.title(f"Module Output - {module_name}")
            output_window.geometry("1080x720")

            # Text widget with scrollbar
            text_frame = ttk.Frame(output_window)
            text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

            output_text = tk.Text(text_frame, wrap=tk.WORD)
            output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            output_text.insert(tk.END, f"Running {function_call}\n")
            output_text.insert(tk.END, "=" * 50 + "\n\n")

            scrollbar = ttk.Scrollbar(text_frame, command=output_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            output_text.config(yscrollcommand=scrollbar.set)

            try:
                sys.stdout = stdout_capture
                sys.stderr = stderr_capture

                # Import and execute the specific module
                try:
                    result = None
                    if module_name == "batch_process":
                        result = batch_process.batch_process("ECHO Images", False)
                    elif module_name == "anova_hsd":
                        result = anova_hsd.main(False)
                    elif module_name == "cleanup_imagej":
                        result = cleanup_imagej.cleanup_imagej(False)
                    elif module_name == "calculate_ed50":
                        # Extract isolate name and plate ID
                        selected_items = self.tree.selection()
                        if not selected_items:
                            result = "No rows selected."
                        else:
                            isolates = []
                            plates = []
                            for item in selected_items:
                                # Exclude runs that didn't pass the quality check
                                if self.tree.set(item, "Quality Check") == "PASS":
                                    isolates.append(self.tree.set(item, "Isolate"))
                                    plates.append(self.tree.set(item, "Plate ID"))
                            result = calculate_ed50.main(isolates, plates, True)
                    elif module_name == "update":
                        result = update.main(False)

                    # If the function returns something, display it
                    if result is not None:
                        output_text.insert(tk.END, f"Return value: {result}\n\n")

                except Exception as e:
                    output_text.insert(tk.END, f"ERROR during execution: {str(e)}\n")
                    output_text.insert(
                        tk.END, f"Traceback:\n{traceback.format_exc()}\n"
                    )
                    self.text_output = str(e)

                # Get captured output
                stdout_value = stdout_capture.getvalue()
                stderr_value = stderr_capture.getvalue()

                if stdout_value:
                    output_text.insert(tk.END, "OUTPUT:\n")
                    output_text.insert(tk.END, stdout_value + "\n")
                    # Pass stdout so it can saved to a file
                    if module_name == "anova_hsd":
                        self.text_output = stdout_value

                if stderr_value:
                    output_text.insert(tk.END, "ERRORS:\n")
                    output_text.insert(tk.END, stderr_value + "\n")
                    # Pass stdout so it can saved to a file
                    self.text_output = stderr_value

                if not stdout_value and not stderr_value:
                    output_text.insert(
                        tk.END, f"{function_call} executed successfully (no output)\n"
                    )

            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

        except Exception as e:
            output_text.insert(tk.END, f"UNEXPECTED ERROR: {str(e)}\n")
            output_text.insert(tk.END, f"Traceback:\n{traceback.format_exc()}\n")
            self.text_output = str(e)

        # Save As Button for statistics tests output or error messages
        if self.text_output:
            ttk.Button(
                output_window, text="Save As", command=self.save_text_output
            ).pack(pady=(0, 10))
        # Close button
        ttk.Button(output_window, text="Close", command=output_window.destroy).pack(
            pady=(0, 10)
        )

        # Show the ouput window
        output_window.deiconify()

        self.open_assay_workbook()
        self.display_sheet()
        self.status_var.set(f"Executed {module_name} module")

    def open_assay_workbook(self):
        """Automatically open the assay workbook and select 'Assay Data' sheet if present"""
        workbook_path = (
            "GPMPhenotypingAssay_Workbook.xlsx"
            if self.current_file is None
            else self.current_file
        )

        # Check if workbook exists in the current directory
        if os.path.exists(workbook_path):
            try:
                self.excel_data = pd.read_excel(workbook_path, sheet_name=None)
                self.current_file = workbook_path

                # Update sheet combo
                sheet_names = list(self.excel_data.keys())
                self.sheet_combo["values"] = sheet_names

                # Try to select "Assay Data" sheet, otherwise use first sheet
                sheet_name = (
                    "Assay Data" if self.current_sheet is None else self.current_sheet
                )
                if sheet_name in sheet_names:
                    self.sheet_var.set(sheet_name)
                    self.current_sheet = sheet_name
                    self.status_var.set(
                        f"Opened: {os.path.basename(workbook_path)} - Sheet: '{sheet_name}'"
                    )
                elif sheet_names:
                    self.sheet_var.set(sheet_names[0])
                    self.current_sheet = sheet_names[0]
                    self.status_var.set(
                        f"Opened: {os.path.basename(workbook_path)} - Sheet: '{sheet_names[0]}' ('{sheet_name}' sheet not found)"
                    )

                self.display_sheet()

            except Exception as e:
                self.status_var.set(f"Error opening {workbook_path}: {str(e)}")
        else:
            self.status_var.set(
                f"Ready - {workbook_path} not found in current directory"
            )


def main():
    """docstring goes here."""
    # Ensure we're running from the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    root = tk.Tk()
    _ = ExcelDataEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
