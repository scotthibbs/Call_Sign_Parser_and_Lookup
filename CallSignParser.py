import tkinter as tk
from tkinter import messagebox

from parser import CallSignParser, CallSignParserError


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


# Verify cty.dat is accessible on startup
try:
    # This will cache the file for future use
    CallSignParser._load_cty_file()
except CallSignParserError as e:
    show_startup_error(str(e))


# Main Program
lbltitle = tk.Label(frame, text="\nCall Sign Look Up")
lbltitle.pack()

# Entry Widget creation
inputent = tk.Entry(frame, width=30, justify="center")
inputent.pack()

# Button Creation
printButton = tk.Button(frame, text="Search", command=printinput1)
printButton.pack()

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
