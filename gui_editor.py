import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import sys
from io import StringIO
import traceback
import pandas as pd

import anova_hsd
import batch_process
import calculate_ed50
import cleanup_imagej
import update


class ExcelDataEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Data Editor - GPM Assay Data")
        self.root.geometry("1080x720")

        self.current_file = None
        self.excel_data = {}
        self.current_sheet = None

        self.setup_ui()
        self.open_assay_workbook()

    def setup_ui(self):
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
        edit_menu.add_command(label="Add Row", command=self.add_row)
        edit_menu.add_command(label="Delete Row", command=self.delete_row)
        edit_menu.add_command(label="Duplicate Row", command=self.duplicate_row)
        edit_menu.add_separator()
        edit_menu.add_command(label="Add Column", command=self.add_column)

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
        self.context_menu.add_command(label="Add Column", command=self.add_column)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Archive Run(s)", command=self.archive_run)
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="Plot ED50(s)", command=self.calculate_ed50_for_row
        )

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
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def open_file(self):
        file_path = filedialog.askopenfilename(
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
        file_path = filedialog.asksaveasfilename(
            title="Save Excel File",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        )

        if file_path:
            self.current_file = file_path
            self.save_file()

    def display_sheet(self):
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
            self.tree.heading(col, text=col)
            self.tree.column(
                col,
                width=120,
                minwidth=80,
                stretch=False
                if any(x in col for x in ("Plate ID", "Quality Check"))
                else True,
            )

        # Insert data (without index)
        for idx, row in df.iterrows():
            values = list(row)
            # Store the actual dataframe index as a tag for internal use
            self.tree.insert("", "end", values=values, tags=(str(idx),))

    def on_sheet_change(self, _=None):
        self.current_sheet = self.sheet_var.get()
        self.display_sheet()

    def get_selected_row_indices(self):
        selections = self.tree.selection()
        if not selections:
            return None

        tags = []
        for item in list(selections):
            tags.append(int(self.tree.item(item, "tags")[0]))
        return tags if tags else None

    def add_row(self):
        if not self.current_sheet:
            messagebox.showwarning("Warning", "No sheet selected")
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
        if not self.current_sheet:
            messagebox.showwarning("Warning", "No sheet selected")
            return

        row_indices = self.get_selected_row_indices()
        if row_indices is None:
            messagebox.showwarning("Warning", "No row(s) selected")
            return

        # Confirm deletion
        if messagebox.askyesno("Confirm", f"Delete row(s) {row_indices}?"):
            for row_index in reversed(row_indices):
                df = self.excel_data[self.current_sheet]
                self.excel_data[self.current_sheet] = df.drop(
                    df.index[row_index]
                ).reset_index(drop=True)

            self.display_sheet()
            self.status_var.set(f"Row(s) {row_indices} deleted")

    def duplicate_row(self):
        if not self.current_sheet:
            messagebox.showwarning("Warning", "No sheet selected")
            return

        row_indices = self.get_selected_row_indices()
        if row_indices is None:
            messagebox.showwarning("Warning", "No row(s) selected")
            return

        for row_index in reversed(row_indices):
            df = self.excel_data[self.current_sheet]
            row_to_duplicate = df.iloc[row_index].copy()

            # Insert duplicated row
            self.excel_data[self.current_sheet] = pd.concat(
                [
                    df.iloc[: row_index + 1],
                    row_to_duplicate.to_frame().T,
                    df.iloc[row_index + 1 :],
                ],
                ignore_index=True,
            )

        self.display_sheet()
        self.status_var.set(f"Row(s) {row_indices} duplicated")

    def add_column(self):
        if not self.current_sheet:
            return

        df = self.excel_data[self.current_sheet]
        col_name = simpledialog.askstring("New Column", "Enter column name:")
        if not col_name:
            return

        if col_name in df.columns:
            tk.messagebox.showerror("Error", f"Column '{col_name}' already exists.")
            return

        # Add a new empty column
        df[col_name] = ""

        self.display_sheet()
        self.status_var.set(f"New Column: {col_name} created")

    def archive_run(self):
        if not self.current_sheet:
            messagebox.showwarning("Warning", "No sheet selected")
            return

        row_indices = self.get_selected_row_indices()
        if row_indices is None:
            messagebox.showwarning("Warning", "No row(s) selected")
            return

        for row_index in reversed(row_indices):
            df = self.excel_data[self.current_sheet]
            row_to_archive = pd.Series(df.iloc[row_index], index=df.columns)
            archive_df = self.excel_data.get("Archived Runs")
            if archive_df is None:
                archive_df = pd.DataFrame(columns=df.columns)
                archive_df = archive_df.astype(df.dtypes.to_dict())

            # Insert duplicated row
            self.excel_data["Archived Runs"] = pd.concat(
                [archive_df, pd.DataFrame([row_to_archive])], ignore_index=True
            )
            # Remove row from Assay Data sheet
            self.excel_data["Assay Data"] = df.drop(df.index[row_index]).reset_index(
                drop=True
            )

        self.display_sheet()
        self.status_var.set(f"Row(s) {row_indices} archived")

    def edit_cell(self, event):
        if not self.current_sheet:
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
            # Try to convert to appropriate type
            try:
                if new_value.isdigit():
                    new_value = int(new_value)
                elif new_value.replace(".", "").isdigit():
                    new_value = float(new_value)
            except:
                pass  # Keep as string

            self.excel_data[self.current_sheet].iloc[row_index, col_index] = new_value
            self.display_sheet()
            self.status_var.set("Cell updated")

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
        # Run the module
        try:
            # Capture stdout/stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr

            stdout_capture = StringIO()
            stderr_capture = StringIO()

            try:
                sys.stdout = stdout_capture
                sys.stderr = stderr_capture

                # Import and execute the specific module
                try:
                    if module_name == "batch_process":
                        result = batch_process.batch_process("ECHO Images", False)
                    elif module_name == "anova_hsd":
                        x, y = pd.Series(), pd.Series()
                        selected_items = self.tree.selection()
                        if len(selected_items) >= 4:
                            df = self.excel_data[self.current_sheet]
                            for i, _ in enumerate(selected_items):
                                item = selected_items[i]
                                index = self.tree.index(item)
                                x.at[i] = df.iloc[index]["Isolate"]
                                y.at[i] = df.iloc[index]["ED50 (J/m^2)"]
                        if 1 <= len(selected_items) <= 3:
                            print(
                                "Select at least 4 runs to perform manual statistical analyses."
                            )
                        result = anova_hsd.main(False, x, y)
                    elif module_name == "cleanup_imagej":
                        result = cleanup_imagej.cleanup_imagej(False)
                    elif module_name == "calculate_ed50":
                        # Extract isolate name and plate ID
                        df = self.excel_data[self.current_sheet]
                        selected_items = self.tree.selection()
                        if not selected_items:
                            result = "No rows selected."
                        else:
                            isolates = []
                            plates = []
                            for i, _ in enumerate(selected_items):
                                item = selected_items[i]
                                index = self.tree.index(item)
                                # Exclude runs that didn't pass the quality check
                                if df.iloc[index]["Quality Check"] == "PASS":
                                    isolates.append(df.iloc[index]["Isolate"])
                                    plates.append(df.iloc[index]["Plate ID"])
                            result = calculate_ed50.main(isolates, plates, True)
                    elif module_name == "update":
                        result = update.main(False)

                    # Create output window
                    output_window = tk.Toplevel(self.root)
                    output_window.title(f"Module Output - {module_name}")
                    output_window.geometry("1080x720")

                    # Text widget with scrollbar
                    text_frame = ttk.Frame(output_window)
                    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

                    output_text = tk.Text(text_frame, wrap=tk.WORD)
                    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                    output_text.insert(tk.END, f"Running {function_call}\n")
                    output_text.insert(tk.END, "=" * 50 + "\n\n")

                    scrollbar = ttk.Scrollbar(text_frame, command=output_text.yview)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    output_text.config(yscrollcommand=scrollbar.set)

                    # If the function returns something, display it
                    if result is not None:
                        output_text.insert(tk.END, f"Return value: {result}\n\n")

                except Exception as e:
                    output_text.insert(tk.END, f"ERROR during execution: {str(e)}\n")
                    output_text.insert(
                        tk.END, f"Traceback:\n{traceback.format_exc()}\n"
                    )

                # Get captured output
                stdout_value = stdout_capture.getvalue()
                stderr_value = stderr_capture.getvalue()

                if stdout_value:
                    output_text.insert(tk.END, "OUTPUT:\n")
                    output_text.insert(tk.END, stdout_value + "\n")

                if stderr_value:
                    output_text.insert(tk.END, "ERRORS:\n")
                    output_text.insert(tk.END, stderr_value + "\n")

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

        # Close button
        ttk.Button(output_window, text="Close", command=output_window.destroy).pack(
            pady=10
        )

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
    # Ensure we're running from the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    root = tk.Tk()
    _ = ExcelDataEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
