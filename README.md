Population_Generator
CS361: Software Engineering I - Winter Term 2021
Ray Franklin

A program to search a data file for a given state and year. It then returns 
the population count for that combination.

To run:

```$ python3 population-generator.py```

Optional arugment:

```$ python3 population-generator.py input.csv```

Note: input.csv takes the format year then state, i.e.
input_year,input_state 2010,Alabama

The program will send the results of the input file to an output.csv file,
it will also output this file when executing the search and append the results.

To communicate:
Option 1 with server/socket connection:
Start the program with 

```$ python3 population-generator.py```

Then also start the Content_Generator.py file from Zekun Chen.

Once both are running, enter data into the primary and secondary key fields then click 
"Request data from Content Generator". It will then show the results in the main text box.

Option 2 with CSV files:
Create the output.csv file by selecting a valid state and year combo then display the results. 
Once the output file is created, the content_generator can search it then produce the output1.csv.
Then click the communicate button to pull in the new data and append it to output.csv.
This should continue to work in order as you create more state year combos, you can append more
data as it is generated by the content_generator.

Dependencies:
python 3.8.5
tkinter 8.6
pandas 0.25.3


