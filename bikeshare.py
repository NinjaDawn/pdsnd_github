import time
import pandas as pd
pd.set_option('display.max_columns', 200)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITY_LIST = ['chicago','new york city','washington']

DAY_LIST = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

MONTH_LIST = ['january', 'february', 'march', 'april', 'may', 'june']



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 

    while True:
           city = input('Which city would you like to explore?: \n Chicago, New York City or Washington? \n> ').lower()
           if city in CITY_LIST:
              break


    # Get user's time filter selection (month, day, or not at all)
    '''Asks the user for a time period and returns the specified filter.
    Args:
        none.
    Returns:
        (list) with two str values:
            filter type: the type of filter period (month, day, or all -no filtering)
            user entry: the specific filter period (ex month: January, example day: Sunday)
    '''
    filter_selection = ''

    while filter_selection.lower() not in ['month','day','all']:
        filter_selection = input('\nWould you like to filter the data by month, day, or all (no filters)?.\n').lower()
        if filter_selection == 'month':
            day = 'all'
            while True:
                month = input('Which month?: January, February, March, April, May, or June? \n').lower()
                if month in MONTH_LIST:
                    break

        elif filter_selection == 'day':
            month = 'all'
            while True:
                day = input('Which day?: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday? \n').lower()
                if day in DAY_LIST:
                    break

        elif filter_selection == 'all':
            # no filtering
            month = 'all'
            day = 'all'
        else:
            print('Unrecognized filter selection: please try again. \n')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month = MONTH_LIST.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # calculate the most common month
    most_frequent_month = df['month'].mode()[0]
    most_frequent_month = MONTH_LIST[most_frequent_month - 1]

    # calculate the most common day of week
    most_frequent_dow = df['day_of_week'].mode()[0]

    # calculate the most common start hour
    most_frequent_start_hour = df['hour'].mode()[0]

    # display calculation results
    print('The most frequent month is :', most_frequent_month.title())
    print('The most frequent day of the week is :', most_frequent_dow)
    print('The most frequent start hour is :', most_frequent_start_hour)
    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # calculate most commonly used start station
    most_common_start = df['Start Station'].mode()[0]

    # calculate most commonly used end station
    most_common_end = df['End Station'].mode()[0]

    # calculate most frequent combination of start station and end station trip
    df['station_combo']=df['Start Station']+" "+"to"+" "+ df['End Station']
    most_common_combo = df['station_combo'].mode()[0]

    # display calculation results
    print('The most popular start station is :', most_common_start)
    print('The most popular end station is :', most_common_end)
    print('The most popular combination of start & end station is:', most_common_combo)
    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration Statistics...\n')
    start_time = time.time()

    # calculate total travel time
    total_travel_time = df['Trip Duration'].sum()


    # calculate mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    # display calculation results
    print("The total travel time in seconds is:", total_travel_time)
    print("The average travel time in seconds:", mean_travel_time)
    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # calculate counts of user types
    user_type_counts= df['User Type'].value_counts()
    # Display calculation results
    print("The bikeshare user types are:\n",user_type_counts)

    # calc and display gender counts for cities with data
    if 'Gender' in df.columns:
        gender_count= df['Gender'].value_counts()
        print('\nThe count for each gender is:\n',gender_count)

    # calc and display the earliest, most recent, and most common birth year
    if 'Birth Year' in df.columns:
        earliest= int(df['Birth Year'].min())
        most_recent= int(df['Birth Year'].max())
        most_common= int(df['Birth Year'].mode()[0])

        # Display calculation results
        print('\nThe earliest birth year is: ',earliest)
        print('The most recent birth year is: ',most_recent)
        print('The most common birth year is: ',most_common)

    print('\nThis took %s seconds.\n' % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays raw data five lines at a time until user chooses to stop."""

    #drop df columns that were not part of original raw data
    df.drop('day_of_week',axis=1,inplace=True)
    df.drop('month',axis=1,inplace=True)
    df.drop('hour',axis=1,inplace=True)
    df.drop('station_combo',axis=1,inplace=True)

    #ask user if they want to see the raw data
    raw_data = input('\nWould you like to see 5 rows of raw trip data?\nType yes or no\n')

    #initialize the variables
    start_row = 0
    answer = True

    #define do while loop
    while (answer):

        #show the 5 rows from data frame
        print(df.iloc[start_row:start_row + 5])

        #increment by 5 for next start row
        start_row += 5

        #Ask user if they want to see more of the raw data
        raw_data = input('\nWould you like to see 5 more rows of data?\n Type yes or no\n').lower()

        #Check the answer, continue if yes and break if no
        if raw_data == "no":
            answer = False
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
