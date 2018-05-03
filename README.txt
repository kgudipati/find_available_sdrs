README

I decided to go with Option 1 and develop and simple CLI to search for sdrs.

Assumptions:
- For simplicity, I have downloaded the the csv file locally and pulling the data from it by default.
- The search query requires to be in the format of {day} {time} {am/pm}.
    - capital/lowercase is fine but spacing must be right
    - eg. ‘mon 2:00 pm’ or ‘Tue 12:00 pm’
- Because of the small data set I decided to use an Interval Tree DS to hold the data, but I would also looked into using dataframes if given more time.
- The program will read the csv file and create the DS every time. In the future, I would use something like the 'pickle' to store the DS internally.

Running Program:
Please pull the code from github: www.github.com/kgudipati/find_available_sdrs
To run the program, simply enter 'python find_available_sdr.py'
