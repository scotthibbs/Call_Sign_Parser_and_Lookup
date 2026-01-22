import tkinter as tk
from tkinter import messagebox

from parser import CallSignParser, CallSignParserError, CtyDownloadError


"""
Python Call Sign Parser with Interface
Copyright (c) 2022 by Scott Anthony Hibbs KD4SIR
Released under a GPLv3 License.
If you do use or modify this software,
I'd really love to hear about it at scott hibbs at gmail dot com.

Type a call sign in the input box and get the result
from the cty.dat file. This can be updated at
https://www.country-files.com/category/big-cty/
maintained with my thanks by Jim Reisert AD1C
- Scott KD4SIR
"""

# Top level window
frame = tk.Tk()
frame.title("Call Sign Parser by Scott Hibbs KD4SIR")
frame.geometry('500x250')


def printinput1():
    """Handle the search button click or Enter key press."""
    # Get input
    inp = inputent.get().strip()

    if len(inp) == 0:
        return

    # Clear previous error styling
    lblreturn.config(fg="black")

    try:
        # Parse the call sign using the parser module
        prefix, separator, suffix, country, is_valid = CallSignParser.parse(inp)

        # Display results
        lblrepeat.config(text=f"\n The original input is: {list(inp)}")
        lblprefix.config(text=f"The prefix is: {prefix}")
        lblseparator.config(text=f"The separator is: {separator}")
        lblsuffix.config(text=f"The suffix is: {suffix}")

        if is_valid:
            lblreturn.config(text=f"This is from: {country}", fg="black")
        else:
            lblreturn.config(text=f"This is from: {country}", fg="orange")

    except CallSignParserError as e:
        # Display error to user
        lblrepeat.config(text="")
        lblprefix.config(text="The prefix:")
        lblseparator.config(text="The separator:")
        lblsuffix.config(text="The suffix:")
        lblreturn.config(text=f"Error: {e}", fg="red")


def show_startup_error(error_msg):
    """Show an error dialog on startup for critical errors."""
    messagebox.showerror("Startup Error", error_msg)


def update_date_label():
    """Update the database date label."""
    date_str = CallSignParser.get_cty_file_date()
    lbldate.config(text=f"Database updated: {date_str}")


def update_database():
    """Download the latest cty.dat file."""
    if messagebox.askyesno("Update Database",
                           "Download the latest cty.dat from country-files.com?"):
        try:
            CallSignParser.download_cty_file()
            update_date_label()
            messagebox.showinfo("Update Complete",
                               "Database updated successfully!")
        except CtyDownloadError as e:
            messagebox.showerror("Update Failed", str(e))


def check_database_age():
    """Check if cty.dat is old and prompt to update."""
    age_days = CallSignParser.get_cty_file_age_days()

    if age_days == -1:
        # File doesn't exist, offer to download
        if messagebox.askyesno("Database Missing",
                               "cty.dat not found. Download now?"):
            try:
                CallSignParser.download_cty_file()
                messagebox.showinfo("Download Complete",
                                   "Database downloaded successfully!")
            except CtyDownloadError as e:
                messagebox.showerror("Download Failed", str(e))
    elif age_days > 30:
        # File is older than 30 days
        if messagebox.askyesno("Database Outdated",
                               f"cty.dat is {age_days} days old.\n"
                               "Download the latest version?"):
            try:
                CallSignParser.download_cty_file()
                messagebox.showinfo("Update Complete",
                                   "Database updated successfully!")
            except CtyDownloadError as e:
                messagebox.showerror("Update Failed", str(e))


# Check database age on startup
check_database_age()

# Verify cty.dat is accessible on startup
try:
    # This will cache the file for future use
    CallSignParser._load_cty_file()
except CallSignParserError as e:
    show_startup_error(str(e))


# Main Program
lbltitle = tk.Label(frame, text="\nCall Sign Look Up")
lbltitle.pack()

# Database date label
lbldate = tk.Label(frame, text="", fg="gray")
lbldate.pack()
update_date_label()

# Entry Widget creation
inputent = tk.Entry(frame, width=30, justify="center")
inputent.pack()

# Button Creation
buttonFrame = tk.Frame(frame)
buttonFrame.pack()

printButton = tk.Button(buttonFrame, text="Search", command=printinput1)
printButton.pack(side=tk.LEFT, padx=5)

updateButton = tk.Button(buttonFrame, text="Update Database", command=update_database)
updateButton.pack(side=tk.LEFT, padx=5)

# Label Creation
lblrepeat = tk.Label(frame, text="")
lblrepeat.pack()

lblprefix = tk.Label(frame, text="The prefix:")
lblprefix.pack()

lblseparator = tk.Label(frame, text="The separator:")
lblseparator.pack()

lblsuffix = tk.Label(frame, text="The suffix:")
lblsuffix.pack()

lblreturn = tk.Label(frame, text="Results:")
lblreturn.pack()

# Bindings
frame.bind('<Return>', (lambda event: printinput1()))

frame.mainloop()
