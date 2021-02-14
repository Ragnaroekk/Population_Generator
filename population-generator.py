# Author: Ray Franklin
# Population Generator CS361
# Built with research from https://realpython.com/python-gui-tkinter/
# and https://realpython.com/python-csv/


from os import read
from tkinter import ttk
import tkinter as tk
import csv
from tkinter.constants import FALSE, TRUE
from typing import Text
import pandas
import sys


YEARS = []
for date in range(1790, 2020, 10):
    YEARS.append(date)

STATES = []
# data from https://worldpopulationreview.com/states/state-abbreviations
with open("/home/ragnaroekk/Documents/Courses/CS361/Population_Generator/csvData.csv", newline='') as file:
    for line in csv.reader(file):
        STATES.append(line[2])

def validate_year(year_input):
    '''Checks the input year to the list of census years'''
    if year_input:
        for year in YEARS:
            if int(year_input) == year:
                return TRUE
    return FALSE

def validate_state(state_input):
    '''Checks the input state abbreviation to the list of 50 states'''
    for state in STATES:
        if state_input == state:
            return TRUE
    return FALSE

# with research from https://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-widget
def get_state():
    '''Returns the state text entered by the user'''
    input = text_box_state.get("1.0", "end-1c")
    return input

def get_year():
    '''Returns the year number entered by the user'''
    input = text_box_year.get("1.0", "end-1c")
    return input

def display_results():
    state = ""
    year = ""

    # check if we got an input file and use those values
    if len(sys.argv) == 2:
        year, state = read_input()
    else:
        # no input file, use text fields
        state = str(get_state())
        year = str(get_year())
    # check for valid inputs
    if not validate_state(state.upper()):
        print("State failue")
        return
    if not validate_year(year):
        print("Year failue")
        return

# with research from https://realpython.com/python-csv/
def read_input():
    data_file = pandas.read_csv(sys.argv[1])
    return data_file["input_year"][0], data_file["input_state"][0]

# main window
window = tk.Tk()
window.resizable(width= 1, height= 1)
window.title("Population Generator")

# user entry for the state and year
text_box_state = tk.Text(height=2, width=10)
text_box_year = tk.Text(height=2, width=10)

# submit button
button = tk.Button(
    text="Display Results!",
    command=lambda: display_results(),
    width=10,
    height=5,
    bg="green",
    fg="white",
)

label_state = tk.Label(text="State:")
label_year = tk.Label(text="Year:")

# wiht research from https://www.askpython.com/python-modules/tkinter
# and https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
tree = ttk.Treeview(window, selectmode="browse")
tree["columns"] = ("1", "2", "3")
tree["show"] = "headings"
tree.heading("1", text="input_year")
tree.heading("2", text="input_state")
tree.heading("3", text="output_population_size")
tree.column("1", stretch=tk.YES)
tree.column("2", stretch=tk.YES)
tree.column("3", stretch=tk.YES)

# add text boxes to the window
label_state.pack()
text_box_state.pack()
label_year.pack()
text_box_year.pack()

# add the button to the window
button.pack()

# add the tree to the window
tree.pack()

# mainloop as required for tkinter
window.mainloop()


