# Author: Ray Franklin
# Population Generator CS361
# Built with research from https://realpython.com/python-gui-tkinter/
# https://realpython.com/python-csv/, https://www.census.gov/data/developers/data-sets/decennial-census.html
# https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html


from os import read, stat
from tkinter import mainloop, ttk
import tkinter as tk
from tkinter.constants import FALSE, TRUE
from typing import Text
import pandas
import sys, os


YEARS = []
for date in range(2010, 2020):
    YEARS.append(date)

STATES = []
# data from https://worldpopulationreview.com/states/state-abbreviations
# help from https://www.tutorialspoint.com/How-to-open-a-file-in-the-same-directory-as-a-Python-script
data_file = pandas.read_csv(os.path.join(sys.path[0],"nst-est2019-01.csv"))
STATES = data_file.iloc[:,0]


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
        if state_input.upper() == state.upper():
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

# with research from https://realpython.com/python-csv/
def read_input():
    data_file = pandas.read_csv(sys.argv[1])
    return data_file["input_year"][0], data_file["input_state"][0]

def display_results(input_received):
    '''Searches the data for the give state and year, then displayes the reult to screen and 
    send it to an output file'''

    # check for an input file
    if input_received:
        year, state = read_input()
    else:
        state = str(get_state())
        year = str(get_year())

    # check for valid inputs
    if not validate_state(state):
        print("State failue")
        return
    if not validate_year(year):
        print("Year failue")
        return
    
    # account for capitalization errors and make sure we have strings
    state = state.capitalize()
    year = str(year)

    # reference https://kanoki.org/2019/04/12/pandas-how-to-get-a-cell-value-and-update-it/
    data_file = pandas.read_csv(os.path.join(sys.path[0], "nst-est2019-01.csv"), index_col=0)
    if not input_received:
        tree.insert("", "end", text="1", values=(year, state, data_file.loc[state][year]))

    df_output = pandas.DataFrame({"year": [year],"state": [state], 
                                "output_population_size": [data_file.loc[state][year]]})
    # research from https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-file
    # appends to current file since input file is overwritten when program is used
    df_output.to_csv("output.csv", mode='a', index=False)

    return

# check if we got an input file and use those values
if __name__ == "__main__":
    if len(sys.argv) == 2:
        display_results(True)

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
    command=lambda: display_results(False),
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




