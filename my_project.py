import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago':'chicago.csv',
    'new york city':'new_york_city.csv',
    'washington':'washington.csv'}

print('\n#Hi, my name is Olanrewaju. It seems you want to explore the bikeshare data.')
def name_city():
    '''
    **This function gets the name of the city**
    **to be anlyzed from the user**
    '''
    print('\n\nI only have data for these three cities: Chicago or c, New York or n, and Washington or w\n\n')
    city = input('Please enter the city you would like to analyze the data for\n   :').title()
    # HINT: Use a while loop to handle invalid inputs
    while True:
            if city == 'Chicago' or city == 'C':
                print("\nGreat! let\'s explore Chicago data together.\n\n")
                return 'chicago'
            elif city == 'New York' or city == 'N':
                print("\nGreat! let\'s explore New York City data together.\n\n")
                return 'new york city'
            elif city == 'Washington' or city == 'W':
                print("\nGreat! let\'s explore Washington data together.\n\n")
                return 'washington'
            else:
                return name_city()
    return city

def load_data(city):
    '''
    This __function__ loads city data **specified** by the user
    to be anlyzed
    '''
    df = pd.read_csv(CITY_DATA[city])
    #Converrting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Extracting the month and day of week from Start Time to create new columns
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    return df

def get_time():
    '''
    the function asks the user to choose time to filter with:
    month or day of the week or no filters
    '''
    print('Type month(m), day(d) or none(n)')
    period = input('\nDo you want to filter the data by month(m) or by day(d) of the week or no filter(n)?\n  :').lower()


    while True:
        if period == "month" or period == "m":
            print('\n The data is now being filtered by month\n')
            return 'month'

        elif period == "day" or period == "d":
            print('\n The data is now being filtered by the day of the week...\n')
            return 'day_of_week'
        elif period == "none" or period == "n":
            print('\n No period filter is being applied to the data\n')
            return "none"
        else:
            return get_time()

def get_month(m):      # get user input for month (january, february, march, april, may, june)
    if m == 'month':
        month = input('\nSelect a month: January, February, March, April, May, or June? Please type out the name in full.\n:  ').strip().lower()
        while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nPlease type the name of the month between January and June? \n  :').strip().lower()
        return month
    else:
        return 'none'


def get_day(d):
    if d == 'day_of_week':
        day = input('\nWhich day? Please type a day M, Tu, W, Th, F, Sa, Su. \n    :').lower().strip()
        while day not in ['m', 'tu', 'w', 'th', 'f', 'sa', 'su']:
            day = input('\nPlease type a day as a choice from M, Tu, W, Th, F, Sa, Su.\n   :').lower().strip()
        return day
    else:
        return 'none'



def time_filters(df, time, month, week_day):

    print('\nCalculating the statisctics from the data loaded. \n')
    #Filtering done by Month
    if time == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filtering done by day of week
    if time == 'day_of_week':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday', 'Sunday']
        for day in days:
            if week_day.capitalize() in day:
                day_of_week = day
        df = df[df['day_of_week'] == day_of_week]

    return df



def month_freq(df):

    print('\n * Q1. What is the most popular month for bike traveling?\n:  ')
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[m - 1].capitalize()
    return popular_month

def day_freq(df):
    #What is the most popular day of week for start time?

    print('\n * Q2. What is the most popular day of the week for bike rides?\n  :')
    return df['day_of_week'].value_counts().reset_index()['index'][0]

def hour_freq(df):
    '''What is the most popular hour of day for start time?
    '''
    print('\n * Q3. What is the most popular hour of the day for bike rides?\n:  ')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]

def ride_duration(df):
    '''
    What is the total ride duration and average ride duration?
    Result:
        tuple = total ride duration, average ride durations
    '''
    # df - dataframe returned from time_filters
    print('\n * Q4. What was the total traveling done for 2017 through June, and what was the average time spent on each trip?\n:  ')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #sum for total trip time, mean for avg trip time
    total_ride_time = np.sum(df['Travel Time'])
    total_days = str(total_ride_time).split()[0]

    print ("\nThe total travel time on 2017 through June was " + total_days + " days \n:  ")
    avg_ride_time = np.mean(df['Travel Time'])
    avg_days = str(avg_ride_time).split()[0]
    print("The average travel time on 2017 through June was " + avg_days + " days \n:  ")

    return total_ride_time, avg_ride_time

def stations_freq(df):
    '''What is the most popular start station and most popular end station?
    '''
    # df - dataframe returned from time_filters
    print("\n* Q5. What is the most popular start station?\n:  ")
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print (start_station)
    print("\n* Q6. What is the most popular end station?\n:  ")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    return start_station, end_station

def common_trip(df):
    '''What is the most popular trip?
    '''
    # df - dataframe returned from time_filters
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n* Q7. What was the most popular trip from start to end?\n:  ')
    return result

def bike_users(df):
    '''What are the counts of each user type?
    '''
     # df - dataframe returned from time_filters
    print('\n* Q8. Types of users: subscribers, customers, others\n:  ')
    return df['User Type'].value_counts()

def gender_data(df):
    '''What are the counts of gender?'''
    # df - dataframe returned from time_filters
    try:
        print('\n* Q9. What is the breakdown of gender among users?\n:  ')
        return df['Gender'].value_counts()
    except:
        print('There is no gender data in the source.')

def birth_years(df):
    '''What is the earliest, latest, and most frequent birth year?'''
    # df - dataframe returned from time_filters
    try:
        print('\n* Q10. What is the earliest, latest, and most frequent year of birth, respectively?\n:  ')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(earliest) + "\n")
        latest = np.max(df['Birth Year'])
        print ("The latest year of birth is " + str(latest) + "\n")
        most_frequent= df['Birth Year'].mode()[0]
        print ("The most frequent year of birth is " + str(most_frequent) + "\n")
        return earliest, latest, most_frequent
    except:
        print('No available birth date data for this period.')

def process(f, df):
    '''Calculates the time it takes to commpute a statistic
    '''
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computing this stat took {}s seconds.".format(time.time() - start_time))

def raw_data_view(df):
    '''
    Displays the raw data used to compute
    the statistics for bikeshare data
    '''
    #drop month column from the dataframe
    df = df.drop(['month'], axis = 1)
    i = 0

    view_data = input("\nWould you like to see the raw data used to compute the statisticss?\n :  ").lower()
    while True:
        if view_data == 'no' or view_data =='n':
            return
        if view_data == 'yes' or view_data =='y':
            print(df[i: i + 5])
            i += 5
        view_data = input("\n Would you like to see more rows of the raw data used to compute the statisticss?\n  :  ").lower()

def main():
    '''The main function calculates and prints out the
    descriptive statistics about a requested city by
    calling all the functions written above
    '''
    city = name_city()
    df = load_data(city)
    period = get_time()
    month = get_month(period)
    day = get_day(period)

    df = time_filters(df, period, month, day)

    # List of all the statistics
    stats_funcs_list = [month_freq,
     day_freq, hour_freq,
     ride_duration, common_trip,
     stations_freq, bike_users, gender_data, birth_years]

    for x in stats_funcs_list:	# displays processing time for each function block
        process(x, df)
    raw_data_view(df)
    # Restarting option
    restart = input("\n * Would you like to do it again and perform another analysis? Type \'yes\' or \'no\'.\n:  ")
    if restart.upper() == 'YES' or restart.upper() == "Y":
        main()

if __name__ == '__main__':
    main()
