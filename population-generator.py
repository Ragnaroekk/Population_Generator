# Author: Ray Franklin
# Population Generator CS361
# Built with research from https://realpython.com/python-gui-tkinter/


from os import read
import tkinter as tk
import csv
from tkinter.constants import FALSE, TRUE
from typing import Text

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
    for year in YEARS:
        if year_input == year:
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
    state = str(get_state())
    print(state)
    if not validate_state(state.upper()):
        print("State failue")
        return
    else:
        print("State accepted")

# main window
window = tk.Tk()
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

# add the button to the grid
button.pack()

label_state = tk.Label(text="State:")
label_state.pack()

# add state text box to the window
text_box_state.pack()
text_box_year.pack()

window.mainloop()