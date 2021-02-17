Population_Generator
CS361: Software Engineering I - Winter Term 2021
Ray Franklin

A program to search a data file for a given state and year. It then returns 
the population count for that combination.

To run:

$ python3 population-generator.py

Optional arugment:
$ python3 population-generator.py input.csv
Note: input.csv takes the format year then state, i.e.
input_year,input_state
2010,Alabama

The program will send the results of the input file to an output.csv file,
it will also output this file when executing the search and append the results.

Dependencies:
tkinter 8.6
pandas 0.25.3


