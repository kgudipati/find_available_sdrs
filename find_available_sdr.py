import csv
from datetime import *
from intervaltree import IntervalTree

"""Helper function to convert 12-HR time to decimal between 0 - 24
"""
def _convertTimeToNumber(time):

    dt = datetime.strptime(time, '%I:%M %p')
    return dt.hour + (dt.minute / 60)


"""Helper function to convert day to number 0 - 4
"""
def _convertDateToNumber(date):

    dates = ["mon", "tue", "wed", "thu", "fri"]
    return dates.index(date)


"""Helper function to convert datetime interval to numeric interval
    
Arguments:
    date {string} -- either range of days or single day
    time {string} -- the time frame
    sdr {string} -- the owner of given datetime interval

Returns:
    interval {list} -- the converted numeric interval(s)
"""
def _convertToNumericIntervals(date, time, sdr):
    date = date.lower()
    time = time.lower()

    # the returned list of intervals
    intervals = list()

    # convert the time to numbers
    times = time.split(" - ")
    lo = _convertTimeToNumber(times[0])
    hi = _convertTimeToNumber(times[1])

    # convert the number intervals based on the given date(s)
    if "-" in date:
        date_int = date.split("-")

        # add the time intervals for each day
        st_idx = _convertDateToNumber(date_int[0])
        end_idx = _convertDateToNumber(date_int[1])

        for i in range(st_idx, end_idx + 1):
            intervals.append( ((24*i) + lo, (24*i) + hi, sdr) )
    
    else:
        date_idx = _convertDateToNumber(date)
        intervals.append( (lo + (24*date_idx), hi + (24*date_idx), sdr) )

    return intervals


"""Get the converted numeric intervals for each given sdr's time frames
    
Arguments:
    sdr {string} -- the owner of given datetime interval
    times {string} -- the datetime frame(s)
    
Returns:
    availability_num_intervals {list} -- the converted numeric interval(s)
"""
def getAvailabilityIntervals(sdr, times):

    # the resulting converted numeric intervals
    availability_num_intervals = list()

    # iterate through each available date-time for current sdr
    for time in times.split(','):

        # extract and separate date and time
        date_time = time.strip().split(" ", 1)
        availability_num_intervals += _convertToNumericIntervals(date_time[0], date_time[1], sdr)
        
    return availability_num_intervals


"""Given a csv_file of sdr's in column 1 and their available timeframes column 2,
    construct an interval to help determine available reps during a searched time slot
    
Arguments:
    csv_filename {string} -- the owner of given datetime interval
    search_datetime {string} -- the datetime frame(s)
    
Returns:
    matching_sdrs {list} -- the list of matching sdr's
"""
def find_available_sdr(csv_filename, search_datetime):
    
    available_intervals = list()

    avail_tree = IntervalTree()

    with open(csv_filename) as csv_file:

        # read in the csv file
        reader = csv.reader(csv_file, delimiter=',')

        for row in reader:
            
            sdr = row[0]
            availability = row[1]
            
            # get a list of converted numeric intervals, 
            # pass sdr to easily keep track of which interval belongs to which sdr
            available_intervals += getAvailabilityIntervals(sdr, availability)
    
    # add the list of intervals to the tree
    for interval in available_intervals:
        avail_tree.insert(interval[0], interval[1], interval[2])


    # convert the given search query to numeric
    date_time = search_datetime.strip().split(" ", 1)
    search_dt = (_convertDateToNumber(date_time[0]) * 24) + _convertTimeToNumber(date_time[1])

    # search the tree to find matching sdrs
    matching_sdrs = list()
    avail_tree.searchMatchingIntervals(avail_tree.root, search_dt, matching_sdrs)

    return matching_sdrs



def main():

    # Prompt the user to search for sdr given a cv file of sdr's and available times
    print("Searching ./sdr_availability.csv...")
    
    datetime = input("Please enter a date time you would like to lookup available sdr's for (eg. 'Wed 10:30 am')\n")
    
    available_sdrs = find_available_sdr('./sdr_availability.csv', str(datetime))

    if len(available_sdrs) == 0:
        print("Sorry No SDR's found for " + str(datetime))
    
    else:
        print("Available SDR's for " + str(datetime) + ":")
        for sdr in available_sdrs:
            print(sdr[2])


if __name__ == "__main__":
    main()