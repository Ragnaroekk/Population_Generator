# Author: Ray Franklin
# Population Generator CS361
# Built and tested with Python 3.8.5
# Built with research from https://realpython.com/python-gui-tkinter/
# https://realpython.com/python-csv/, https://www.census.gov/data/developers/data-sets/decennial-census.html
# https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html


from tkinter import ttk
import tkinter as tk
from tkinter.constants import FALSE, TRUE
import pandas
import sys, os
from os import path
import socket
from multiprocessing import Process


# years from available data, 2010 through 2019
YEARS = []
for date in range(2010, 2020):
    YEARS.append(date)

STATES = []
# data from https://worldpopulationreview.com/states/state-abbreviations
# help from https://www.tutorialspoint.com/How-to-open-a-file-in-the-same-directory-as-a-Python-script
data_file = pandas.read_csv(os.path.join(sys.path[0],"nst-est2019-01.csv"))
STATES = data_file.iloc[:,0]


# separated out GUI from server
def GUI():
    def validate_year(year_input):
        '''Checks the input year to the list of census years
        Returns: False if not found, true otherwise'''
        if year_input:
            for year in YEARS:
                if int(year_input) == year:
                    return TRUE
        return FALSE

    def validate_state(state_input):
        '''Checks the input state's name to the list of 50 states
        Returns: False if not found, true otherwise'''
        for state in STATES:
            if state_input.upper() == state.upper():
                return TRUE
        return FALSE

    # with research from https://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-widget
    def get_state():
        '''Returns the state text entered by the user'''
        input = text_box_state.get()
        return input

    def get_year():
        '''Returns the year number entered by the user'''
        input = text_box_year.get()
        return input

    def get_data_file(csv_file):
        '''A method to read a local csv file into a pandas data file
        Returns: a Pandas data file'''
        data_file = pandas.read_csv(os.path.join(sys.path[0], str(csv_file)), index_col=0)
        return data_file

    # with research from https://realpython.com/python-csv/
    def read_input():
        '''Reads in a csv file passed in as an arg
        Returns: a data file tuple with year and state'''
        data_file = pandas.read_csv(sys.argv[1])
        return data_file["input_year"][0], data_file["input_state"][0]

    def check_for_input(input_received):
        '''Checks the system for passed in aruguments or text entry
        Returns: a tuple with the state then year'''
        # check for an input file
        if input_received:
            return read_input()
        else:
            return str(get_year()), str(get_state())

    def validate_inputs(state, year):
        '''Checks for valid inputs, prints error message if state or year is not found
        Returns: False if issues are found, True otherwise'''
        if not validate_state(state):
            text_box_socket.insert("end","State failure\n")
            return False
        if not validate_year(year):
            text_box_socket.insert("end","Year failure\n")
            return False
        return True

    def output_results_to_csv(state, year, data_file):
        '''Takes population data for the given state and year send it to an output file'''
        # send our new data to the output file
        df_output = pandas.DataFrame({"year": [year], "state": [state],
                                      "output_population_size": [data_file.loc[state][year]], "output_content": ""})
        # research from:
        # https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-file
        # creates output file if with headers if not found, or appends the results
        if path.exists("output.csv"):
            df_output.to_csv("output.csv", mode='a', index=False, header=False)
        else:
            df_output.to_csv("output.csv", mode='a', index=False)
        return

    def display_results(input_received):
        '''Takes population data for the given state and displays it'''
        # taken in from user input
        year, state = check_for_input(input_received)
        if not validate_inputs(state, year):
            return

        # account for capitalization errors and make sure we have strings
        state = state.capitalize()
        year = str(year)

        # reference https://kanoki.org/2019/04/12/pandas-how-to-get-a-cell-value-and-update-it/
        data_file = get_data_file("nst-est2019-01.csv")
        if not input_received:
            tree.insert("", "end", text="1", values=(year, state, data_file.loc[state][year]))

        output_results_to_csv(state, year, data_file)

        return

    def keep_count(function):
        '''Wrapper to track how many times a function is called'''
        # https://realpython.com/primer-on-python-decorators/
        def wrapper():
            wrapper.called += 1
            return function()
        wrapper.called = 0
        return wrapper

    @keep_count
    def append_results():
        '''Takes the external data and appends it to the output file'''
        # research from
        # https://www.kite.com/python/answers/how-to-add-a-column-to-a-csv-file-in-python
        try:
            input_file = get_data_file("output" + str(append_results.called) + ".csv")
            data_from_content_generator = input_file.iloc[0, 1]
            output_file = get_data_file("output.csv")
            output_file.iloc[append_results.called - 1, 2] = data_from_content_generator
            output_file.to_csv("output.csv")
        except:
            text_box_socket.insert("end","Issue Reading File")
            append_results.called -= 1
        return

    def check_key_entry(key):
        '''Checks the text entry for empty boxes
        Returns: True if length is longer than 0, False otherwise'''
        if len(key) > 0:
            return True
        else:
            return False

    def request_content():
        '''Sends a request to the Content Generator with primary and secondary key as entered by user
        Returns: None, but will display the response data from the content generator
        '''
        # research from https://stackoverflow.com/questions/42473873/
        primary_key = text_box_primary.get()
        secondary_key = text_box_secondary.get()
        
        if not check_key_entry(primary_key):
            text_box_socket.insert("end", "Missing primary or secondary text entry")
            return 

        # research from https://wiki.python.org/moin/HandlingExceptions
        # https://stackoverflow.com/questions/27966626/how-to-clear-delete-the-contents-of-a-tkinter-text-widget
        # and https://realpython.com/python-sockets/
        try:
            text_box_socket.delete(1.0, tk.END)
            client = socket.socket()
            client.connect(("localhost", 8000))
            message = primary_key + ',' + secondary_key  # format requested by content generator
            text_box_socket.insert("end", "Population Generator is requesting data...\n")
            client.send(message.encode())
            data = client.recv(1024)
            data=data.decode()
            text_box_socket.insert("end", "Content generated: " + data + ".\n")
        except Exception as error:
            text_box_socket.delete(1.0, tk.END)
            text_box_socket.insert("end", str(error) + '\n')

    # process optional input.csv file
    if len(sys.argv) == 2:
        display_results(True)

    # tkinter section with research from https://realpython.com/python-gui-tkinter/
    # and https://www.tutorialspoint.com/python/tk_entry.htm
    # main window
    window = tk.Tk()
    window.resizable(width= 1, height= 1)
    window.title("Population Generator")

    # text and entry boxes
    text_box_state = tk.Entry(window)
    text_box_year = tk.Entry(window)
    text_box_primary = tk.Entry(window)
    text_box_secondary = tk.Entry(window)
    text_box_socket = tk.Text(height=7, width=45)
 
    # primary button for search execution
    button_submit = tk.Button(
        text="Display Results!",
        command=lambda: display_results(False),
        width=10,
        height=5,
        bg="green",
        fg="white",
    )

    # secondary button for csv read and write
    button_communicate = tk.Button(
        text="Communicate with CSV",
        command=lambda: append_results(),
        width=20,
        height=3,
        bg="grey",
        fg="black",
    )

    # for socket communication back and forth
    button_request = tk.Button(
        text="Request data from Content Generator",
        command=request_content,
        width=30,
        height=3,
        bg="grey",
        fg="black",
    )

    # text field lables
    label_state = tk.Label(text="Full State Name:")
    label_year = tk.Label(text="Year 2010-2019:")
    label_socket = tk.Label(text="Communication Information:")
    label_primary = tk.Label(text="Content Generator Primary key:")
    label_secondary = tk.Label(text="Content Generator Secondary key:")

    # with research from https://www.askpython.com/python-modules/tkinter
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
    label_primary.pack()
    text_box_primary.pack()
    label_secondary.pack()
    text_box_secondary.pack()
    label_socket.pack()
    text_box_socket.pack()

    # add the buttons to the window
    button_submit.pack()
    button_communicate.pack()
    button_request.pack()

    # add the tree to the window
    tree.pack()

    # mainloop as required for tkinter
    window.mainloop()

def get_population_size(state,year):
    '''Finds the population size of a state and year
    Returns: the population as a string'''
    data = pandas.read_csv("nst-est2019-01.csv",index_col=0)
    state = state.capitalize()
    if state not in data.index:
        return "State failure"
    if year not in data.columns:
        return "Year failure"
    return str(data.loc[state,year])

def communication_server():
    '''
    Receives new state and year requests and sends back the population
    Returns: none
    '''
    # help from https://pythonprogramming.net/sockets-tutorial-python-3/
    server = socket.socket()
    server.bind(("localhost", 9999))
    server.listen()

    while True:
        conn, addr = server.accept()
        print("New connection:", addr)
        data = conn.recv(1024)
        data=data.decode()
        print("Received data:", data)
        population=get_population_size(data.split(',')[0],data.split(',')[1])
        print(population)
        conn.send(population.encode())

# modeled after Zekun Chen's layout
if __name__=="__main__":


    gui_process = Process(target = GUI)
    server_process = Process(target = communication_server)
    gui_process.start()
    server_process.start()
    gui_process.join()
