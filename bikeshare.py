import calendar as cr
import numpy as np
import os
import pandas as pd
import time

path = os.path.dirname(__file__)

CITY_DATA = {
    'chicago': path + '/chicago.csv',
    'new york city': path + '/new_york_city.csv',
    'washington': path + '/washington.csv'
}
cities = ['chicago', 'new york city', 'washington']
days = list(range(0, 8))
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']


def get_filter_condition():
    """
    The user enters information about a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let is explore some US bikeshare data!")
    city = check_city()

    while True:
        choice = input(
            "Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter.\n").lower()

        # check input to get correct information about the month and day.
        if choice == 'month':
            day = 'all'
            month = check_month()
        elif choice == 'day':
            day = check_day()
            month = 'all'
        elif choice == 'both':
            day = check_day()
            month = check_month()
        elif choice == 'none':
            day = 'all'
            month = 'all'
        else:
            print("The value entered is incorrect.")
            day = ''
            month = ''
        break
    print('*'*50)
    return city, month, day


def check_city():
    """
    The user enters information about a city to analyze.

    Returns:
        (str) city - name of the city to analyze 
    """

    city = input(
        "Would you like to to see data for Chicago, New York City, or Washington?\n").lower()
    if city not in cities:
        print("Invalid city name. Please choose either 'Chicago', 'New York City', or 'Washington'.")
        city = ''
    return city


def check_month():
    """
    The user enters information about a month to analyze.

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """

    month = input(
        "Which month? January, February, March, April, May, or June? You can enter 'All' to get all months.\n").lower()
    if month not in months:
        print("Invalid month. Please choose either All, January, February, March, April, May, or June.")
        month = ''
    return month


def check_day():
    """
    The user enters information about a day to analyze.

    Returns:
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    day = int(input(
        "Which day? Please type your response as an integer(e.g... 0=Monday). You can enter '7' to get all days.\n"))
    if day not in days:
        print('Invalid day. Please choose either from 0 to 7.')
        day = ''
    elif day == 7:
        day = 'all'
    else:
        day = cr.day_name[day]
    return day.lower()


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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def times_of_travel(df):
    """
    Shows statistics about the most popular travel of times.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    start_time = time.time()
    print('\nPopular times of travel: ')

    # show the most common month.
    month_of_travel = cr.month_name[df['month'].mode()[0]]
    print('Most Common Month: \n', month_of_travel)

    # show the most common day of week.
    day_of_travel = df['day_of_week'].mode()[0]
    print('Most Common Day of Week: \n', day_of_travel)

    # show the most common hour of day.
    df['hour'] = df['Start Time'].dt.hour
    hour_of_travel = df['hour'].mode()[0]
    print('Most Common Hour of Day: \n', str(hour_of_travel) + ':00:00')

    print("\nThat took %s seconds." % (time.time() - start_time))
    print('*'*50)


def stations_and_trip(df):
    """
    Shows statistics about the most popular station and trip.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    start_time = time.time()
    print('\nPopular stations and trip: ')

    # show the most common start station.
    start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station: \n", start_station)

    # show the most common end station.
    end_station = df['End Station'].mode()[0]
    print("Most Common End Station: \n", end_station)

    # show the most common trip from start to end.
    frequent_station = "From " + \
        df['Start Station'] + " to " + df['End Station']
    station = frequent_station.mode()[0]
    print("Most Common Trip from Start to End: \n", station)

    print("\nThat took %s seconds." % (time.time() - start_time))
    print('*'*50)


def trip_duration(df):
    """
    Shows statistics about the most popular trip duration.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    start_time = time.time()
    print('\nTrip duration:')

    # show the total travel time.
    total_trip_duration = df['Trip Duration'].sum()
    total_minute, total_second = divmod(total_trip_duration, 60)
    total_hour, total_minute = divmod(total_minute, 60)
    print("Total Travel Time: \n", str(round(total_hour)) + ':' +
          str(round(total_minute)) + ':' + str(round(total_second)))

    # show the average travel time.
    average_duration = round(df['Trip Duration'].mean())
    average_minute, average_second = divmod(average_duration, 60)
    average_hour, average_minute = divmod(average_minute, 60)
    print("Average Travel Time: \n", str(round(average_hour)) + ':' +
          str(round(average_minute)) + ':' + str(round(average_second)))

    print("\nThat took %s seconds." % (time.time() - start_time))
    print('*'*50)


def user_info(df, city):
    """
    Shows statistics about user info.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        city - name of the city to analyze
    """

    start_time = time.time()
    print('\nUser info: ')

    # show the information user type
    user_type = df['User Type'].value_counts()
    print("Counts of Each User Type: ")
    print('Subscriber: ', user_type['Subscriber'])
    print('Customer: ', user_type['Customer'])

    # show the information of gender and birth year if the city is Chicago or New York City
    if city in ['chicago', 'new york city']:
        gender = df['Gender'].value_counts()
        print('\nCounts of Each Gender: ')
        print('Male: ', gender['Male'])
        print('Female: ', gender['Female'])

        print('\nEarliest Year of Birth: ', int(df['Birth Year'].min()))
        print('Most Recent Year of Birth: ', int(df['Birth Year'].max()))
        print('Most Common Year of Birth: ', int(df['Birth Year'].mode()[0]))

    print("\nThat took %s seconds." % (time.time() - start_time))
    print('*'*50)


def show_more_data(df, city):
    """
    Shows more individual trip data.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        city - name of the city to analyze
    """

    df_length = len(df.index)
    df.drop(['month', 'day_of_week', 'hour'], axis=1, inplace=True)

    start_number = 0
    page_length = 5

    while start_number < df_length:
        raw_data = input(
            "\nWould you like to view individual trip data? Type 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            if start_number+page_length > df_length:
                show_single_data(df, start_number, df_length, city)
            else:
                show_single_data(df, start_number, start_number + page_length, city)
            start_number += 5
        else:
            break


def show_single_data(df, start_number, end_number, city):
    range_data = [*range(start_number, end_number, 1)]
    np.array([format_single_data(df, i, city) for i in range_data])


def format_single_data(df, line_number, city):
    data = df.iloc[line_number]
    print('*'*50)
    print('\nNo.: ', data[0])
    print('Start Time: ', data['Start Time'])
    print('End Time: ', data['End Time'])
    print('Trip Duration: ', data['Trip Duration'])
    print('Start Station: ', data['Start Station'])
    print('User Type: ', data['User Type'])
    if city in ['chicago', 'new york city']:
        print('Gender: ', data['Gender'])
        print('Birth Year: ', data['Birth Year'])


def main():
    while True:
        city, month, day = get_filter_condition()
        if city == '' or month == '' or day == '':
            print('Please enter the correct value.')
        else:
            print("You selected {}, {}, and {}.".format(
                city.title(), month.title(), day.title()))

            df = load_data(city, month, day)

            times_of_travel(df)
            stations_and_trip(df)
            trip_duration(df)
            user_info(df, city)
            show_more_data(df, city)

        restart = input("\nWould you like to restart? Type 'yes' or 'no'.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
