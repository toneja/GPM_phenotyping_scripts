import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        self.root.title("Excel Data Editor - Assay Data")
        self.root.geometry("1080x720")

        # Initialize variables
        self.df = None
        self.excel_file = "GPMPhenotypingAssay_Workbook.xlsx"
        self.sheet_name = "Assay Data"

        # Create the GUI
        self.create_widgets()

        # Try to load the Excel file on startup
        self.load_excel_data()

    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # Make the tree frame expandable

        # File operations frame
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)  # Make the entry field expandable

        # File path label and entry
        ttk.Label(file_frame, text="Excel File:").grid(row=0, column=0, padx=(0, 5))
        self.file_path_var = tk.StringVar(value=self.excel_file)
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var)
        file_entry.grid(row=0, column=1, padx=(0, 5), sticky=(tk.W, tk.E))

        # Buttons
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(
            row=0, column=2, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Save", command=self.save_excel_data).grid(
            row=0, column=3, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Add Row", command=self.add_row).grid(
            row=0, column=4, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Delete Row", command=self.delete_row).grid(
            row=0, column=5, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Duplicate Row", command=self.duplicate_row).grid(
            row=0, column=6, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Get Results", command=self.get_results).grid(
            row=0, column=7, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Get Stats", command=self.get_stats).grid(
            row=0, column=8, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Clean Files", command=self.cleanup_imagej).grid(
            row=0, column=9, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Update Code", command=self.update_code).grid(
            row=0, column=10
        )

        # Status label (separate row)
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))

        # Create treeview for data display
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Treeview with scrollbars
        self.tree = ttk.Treeview(tree_frame)

        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
            tree_frame, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(xscrollcommand=h_scrollbar.set)

        # Grid treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Bind events for editing
        self.tree.bind("<Double-1>", self.on_item_double_click)
        self.tree.bind("<Return>", self.on_item_double_click)
        self.tree.bind("<F2>", self.on_item_double_click)

        # Bind right-click for context menu
        self.tree.bind(
            "<Button-3>", self.show_context_menu
        )  # Right-click on Windows/Linux
        self.tree.bind("<Button-2>", self.show_context_menu)  # Right-click on Mac

        # Create context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(
            label="Calculate ED50", command=self.calculate_ed50_for_row
        )

    def browse_file(self):
        """Open file dialog to select Excel file"""
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        )
        if filename:
            self.file_path_var.set(filename)
            self.excel_file = filename
            # Automatically load the new file
            self.load_excel_data()

    def load_excel_data(self):
        """Load data from Excel file"""
        try:
            self.excel_file = self.file_path_var.get()

            if not os.path.exists(self.excel_file):
                self.status_var.set(f"File not found: {self.excel_file}")
                return

            # Read the Excel file
            self.df = pd.read_excel(self.excel_file, sheet_name=self.sheet_name)

            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Configure columns
            columns = list(self.df.columns)
            self.tree["columns"] = columns
            self.tree["show"] = "headings"

            # Configure column headings and widths
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, minwidth=50)

            # Insert data
            for index, row in self.df.iterrows():
                values = [str(val) if pd.notna(val) else "" for val in row]
                self.tree.insert("", "end", values=values, tags=(index,))

            self.status_var.set(
                f"Loaded {len(self.df)} Assay Runs from {self.sheet_name}"
            )

        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{self.excel_file}' not found.")
            self.status_var.set("File not found")
        except ValueError as e:
            if "Worksheet named" in str(e):
                messagebox.showerror(
                    "Error", f"Sheet '{self.sheet_name}' not found in the Excel file."
                )
                self.status_var.set("Sheet not found")
            else:
                messagebox.showerror("Error", f"Error reading Excel file: {str(e)}")
                self.status_var.set("Error reading file")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            self.status_var.set("Error")

    def save_excel_data(self):
        """Save current data back to Excel file"""
        if self.df is None:
            messagebox.showwarning(
                "Warning", "No data to save. Please load data first."
            )
            return

        try:
            # Get current data from treeview
            data = []
            for item in self.tree.get_children():
                values = self.tree.item(item)["values"]
                data.append(values)

            # Create new DataFrame
            columns = list(self.df.columns)
            new_df = pd.DataFrame(data, columns=columns)

            # Convert empty strings back to NaN for proper Excel formatting
            new_df = new_df.replace("", pd.NA)

            # Fix up dtypes
            for column in new_df.columns:
                if any(col in column for col in ["Irradiance", "Lamp", "Time"]):
                    new_df[column] = pd.to_numeric(new_df[column], errors="coerce")

            # Save to Excel (this will overwrite the specific sheet)
            with pd.ExcelWriter(
                self.excel_file, engine="openpyxl", mode="a", if_sheet_exists="replace"
            ) as writer:
                new_df.to_excel(writer, sheet_name=self.sheet_name, index=False)

            self.df = new_df
            self.status_var.set(f"Data saved to {self.excel_file}")
            messagebox.showinfo("Success", "Data saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")
            self.status_var.set("Save failed")

    def add_row(self):
        """Add a new empty row"""
        if self.df is None:
            messagebox.showwarning("Warning", "Please load data first.")
            return

        # Create empty row with same number of columns
        empty_values = [""] * len(self.df.columns)
        self.tree.insert("", "end", values=empty_values)
        self.status_var.set("New row added")

    def delete_row(self):
        """Delete selected row"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a row to delete.")
            return

        for item in selected_items:
            self.tree.delete(item)

        self.status_var.set(f"Deleted {len(selected_items)} row(s)")

    def duplicate_row(self):
        """Duplicate a selected row"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a row to duplicate.")
            return

        for item in selected_items:
            self.tree.insert("", "end", values=self.tree.item(item, "values"))

        self.status_var.set(f"Duplicated {len(selected_items)} row(s)")

    def get_results(self):
        """Batch process images with ImageJ and analyze output"""
        # Path to data
        file_path = "ECHO Images"

        # Update status
        self.status_var.set("Batch processing images...")
        self.root.update()

        # Capture stdout to get the output from the script
        old_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Execute the batch_process.batch_process() function
            batch_process.batch_process(file_path, False)

            # Get the captured output
            output = captured_output.getvalue()

        except Exception as e:
            output = f"Error executing batch_process.batch_process(): {str(e)}\n{traceback.format_exc()}"
        finally:
            # Restore stdout
            sys.stdout = old_stdout

        # Show the output to the user
        self.show_output_dialog("Results Generation", output)

        self.status_var.set("Image processing complete.")

        # Update the workbook data
        filename = "GPMPhenotypingAssay_Workbook.xlsx"
        if os.path.exists(filename):
            self.file_path_var.set(filename)
            self.excel_file = filename
            # Automatically load the updated file
            self.load_excel_data()

    def get_stats(self):
        """Perform one-way ANOVA and Tukey's HSD tests"""
        # Update status
        self.status_var.set("Performing statistical analyses...")
        self.root.update()

        # Capture stdout to get the output from the script
        old_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Execute the anova_hsd.main() function
            anova_hsd.main(False)

            # Get the captured output
            output = captured_output.getvalue()

        except Exception as e:
            output = (
                f"Error executing anova_hsd.main(): {str(e)}\n{traceback.format_exc()}"
            )
        finally:
            # Restore stdout
            sys.stdout = old_stdout

        # Show the output to the user
        self.show_output_dialog("Statistical Analyses", output)

        self.status_var.set("Statistical analyses complete.")

    def cleanup_imagej(self):
        """Delete all temporary files created by ImageJ"""
        # Update status
        self.status_var.set("Cleaning up ImageJ files...")
        self.root.update()

        # Capture stdout to get the output from the script
        old_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Execute the anova_hsd.main() function
            cleanup_imagej.cleanup_imagej(False)

            # Get the captured output
            output = captured_output.getvalue()

        except Exception as e:
            output = f"Error executing cleanup_imagej.cleanup_imagej(): {str(e)}\n{traceback.format_exc()}"
        finally:
            # Restore stdout
            sys.stdout = old_stdout

        # Show the output to the user
        self.show_output_dialog("ImageJ File Cleanup", output)

        self.status_var.set("ImageJ file cleanup complete.")

    def update_code(self):
        """Download latest version of this project from GitHub"""
        # Update status
        self.status_var.set("Updating files to the latest version...")
        self.root.update()

        # Capture stdout to get the output from the script
        old_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Execute the anova_hsd.main() function
            update.main(False)

            # Get the captured output
            output = captured_output.getvalue()

        except Exception as e:
            output = (
                f"Error executing update.main(): {str(e)}\n{traceback.format_exc()}"
            )
        finally:
            # Restore stdout
            sys.stdout = old_stdout

        # Show the output to the user
        self.show_output_dialog("Code Update", output)

        self.status_var.set("Code update Complete. Restart the program.")

    def on_item_double_click(self, event):
        """Handle double-click, Enter, or F2 to edit cell"""
        if not self.tree.selection():
            return

        item = self.tree.selection()[0]

        # If it's a keyboard event, use the first column by default
        if event.keysym in ["Return", "F2"]:
            col_index = 0
        else:
            # For mouse events, identify the clicked column
            column = self.tree.identify_column(event.x)
            if not column:
                return
            # Get column index (subtract 1 because identify_column returns 1-based index)
            col_index = int(column.replace("#", "")) - 1

        # Get current value
        current_values = list(self.tree.item(item)["values"])
        current_value = (
            current_values[col_index] if col_index < len(current_values) else ""
        )

        # Get column name for the dialog title
        if self.df is not None and col_index < len(self.df.columns):
            column_name = self.df.columns[col_index]
        else:
            column_name = f"Column {col_index + 1}"

        # Create edit dialog
        self.edit_cell(item, col_index, current_value, column_name)

    def edit_cell(self, item, col_index, current_value, column_name="Cell"):
        """Create dialog to edit cell value"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit {column_name}")
        dialog.geometry("350x150")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.geometry(
            "+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50)
        )

        # Main frame
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Labels
        ttk.Label(main_frame, text=f"Editing: {column_name}").pack(pady=(0, 5))
        ttk.Label(main_frame, text="Enter new value:").pack(pady=(0, 5))

        # Entry widget with better styling
        entry_var = tk.StringVar(value=str(current_value))
        entry = ttk.Entry(
            main_frame, textvariable=entry_var, width=40, font=("TkDefaultFont", 10)
        )
        entry.pack(pady=5, fill=tk.X)
        entry.focus()
        entry.select_range(0, tk.END)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10, fill=tk.X)

        def save_edit():
            new_value = entry_var.get()
            current_values = list(self.tree.item(item)["values"])

            # Ensure we have enough values in the list
            while len(current_values) <= col_index:
                current_values.append("")

            current_values[col_index] = new_value
            self.tree.item(item, values=current_values)

            # Update status
            row_num = self.tree.index(item) + 1
            self.status_var.set(f"Updated {column_name} in row {row_num}")

            dialog.destroy()

        def cancel_edit():
            dialog.destroy()

        # Create buttons with better layout
        ttk.Button(button_frame, text="Save", command=save_edit).pack(
            side=tk.RIGHT, padx=(5, 0)
        )
        ttk.Button(button_frame, text="Cancel", command=cancel_edit).pack(side=tk.RIGHT)

        # Bind keyboard shortcuts
        entry.bind("<Return>", lambda e: save_edit())
        entry.bind("<Escape>", lambda e: cancel_edit())
        dialog.bind("<Return>", lambda e: save_edit())
        dialog.bind("<Escape>", lambda e: cancel_edit())

    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the item under the cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            # Show context menu at cursor position
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()

    def calculate_ed50_for_row(self):
        """Calculate ED50 for the selected row"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a row.")
            return

        if self.df is None:
            messagebox.showwarning("Warning", "No data loaded.")
            return

        try:
            # Get the selected row data
            item = selected_items[0]
            row_values = self.tree.item(item)["values"]

            # Create a dictionary mapping column names to values
            row_data = {}
            columns = list(self.df.columns)
            for i, col in enumerate(columns):
                if i < len(row_values):
                    row_data[col] = row_values[i]
                else:
                    row_data[col] = ""

            # Extract Plate ID and Isolate
            plate_id = row_data.get("Plate ID", "")
            isolate = row_data.get("Isolate", "")

            if not plate_id or not isolate:
                messagebox.showerror(
                    "Error",
                    "Could not find 'Plate ID' and/or 'Isolate' columns in the data.\n\n"
                    f"Available columns: {', '.join(columns)}\n"
                    f"Plate ID: '{plate_id}'\n"
                    f"Isolate: '{isolate}'",
                )
                return

            # Update status
            self.status_var.set(f"Calculating ED50 for {isolate} {plate_id}...")
            self.root.update()

            # Capture stdout to get the output from the script
            old_stdout = sys.stdout
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                # Execute the calculate_ed50.main function
                calculate_ed50.main(isolate, plate_id, True)

                # Get the captured output
                output = captured_output.getvalue()

            except Exception as e:
                output = f"Error executing calculate_ed50.main(): {str(e)}\n{traceback.format_exc()}"
            finally:
                # Restore stdout
                sys.stdout = old_stdout

            # Automatically load the updated file
            self.load_excel_data()

            # Show the output to the user
            self.show_output_dialog("ED50 Calculation", output)

            self.status_var.set(f"ED50 calculation completed for {isolate} {plate_id}")

        except Exception as e:
            messagebox.showerror("Error", f"Error during ED50 calculation: {str(e)}")
            self.status_var.set("ED50 calculation failed")

    def show_output_dialog(self, action, output):
        """Show the output from actions in a dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{action} Results")
        dialog.geometry("600x400")
        dialog.transient(self.root)

        # Center the dialog
        dialog.geometry(
            "+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100)
        )

        # Main frame
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text=f"Results for: {action}",
            font=("TkDefaultFont", 10, "bold"),
        )
        title_label.pack(pady=(0, 10))

        # Text widget with scrollbar for output
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Courier", 9),
            fg="#00FF00",
            bg="black",
            insertbackground="#00FF00",
        )
        scrollbar = ttk.Scrollbar(
            text_frame, orient="vertical", command=text_widget.yview
        )
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert the output
        if output.strip():
            text_widget.insert(tk.END, output)
        else:
            text_widget.insert(tk.END, f"No output generated by {action}")

        text_widget.config(state=tk.DISABLED)  # Make it read-only

        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=dialog.destroy)
        close_button.pack(pady=(10, 0))


def main():
    # Ensure we're running from the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    root = tk.Tk()
    _ = ExcelDataEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
