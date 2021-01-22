"""
PROJECT 2: Explore US Bikesare Data

This project explores data related to bike share systems for three major cities in the US:
    - Chicago           - Washington
    - New York City

The code answers interesting questions about it by computing descriptive statistics.
The code will take raw input to create an interactive experience in the terminal
to present these statistics.

"""

import os
import time
import pandas as pd
import numpy as np


CITY_DATA = {'chicago': 'bikeshare_files/chicago.csv',
             'new york city': 'bikeshare_filesnew_york_city.csv',
             'washington': 'bikeshare_files/washington.csv'}


def call_title():
    '''Print the heading for the program'''
    print('-'*44)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*44)
    print()
    return


def city_check(city):
    '''simplify checking the city so the user does not have to type city name'''
    if city == 'c':
        return 'chicago'
    elif city == 'n':
        return 'new york city'
    elif city == 'w':
        return 'washington'
    else:
        return 'nada'


def cal_check(frag, section):
    'check to ensure that the month or day entered by the user is in this list'
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    if frag == 'm':
        if section in months:
            return section
    elif frag == 'd':
        if section in days:
            return section


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington).

    while True:
        os.system('clear')
        call_title()
        city = str(input('Which city do you want to search, Enter [c] - Chicago, [n] - New York City or [w] - Washington: ')).lower()
        city = city_check(city.lower())
        if city in CITY_DATA:
            time.sleep(.5)
            print('You have selected {}. '.format(city.title()))
            time.sleep(.5)

            while True:
                month = str(input('Enter the month you wish to investigate - or enter \'all\': '))
                if month == cal_check('m', month):
                    break
                else:
                    print('\n     \'{}\' is not a month in the dataset..\n'.format(month))
                    continue

            while True:
                day = str(input('Enter the day do you want to investigate - or enter \'all\': '))
                if day == cal_check('d', day):
                    break
                else:
                    print('\n     \'{}\' is not a day in dataset..\n'.format(day))

            # Ask user to verify their choice
            print('\nYou will be investigaing the city of {} --> month(s): {} --> day(s): {}'
                  .format(city.title(), month.title(), day.title()))

            dec = str(input('Are you sure? (y, anykey to cancel) ')).lower()
            if dec == 'y':
                print('-'*44)
                return city, month, day
                break
                break
            else:
                print('restarting..')
                time.sleep(4)

        else:
            time.sleep(1)
            print('Hmmm...')
            # # TODO:
            # make time
            print('That city is not in the database...')
            time.sleep(4)


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def view_data(df):
    '''allow the user to explore 5 individual rows of travel data in a tabular data '''
    print()
    start_loc = 0
    while True:
        to_view = str(input('Do you wish to view 5 rows of individual travel data? (y/n) ')).lower()
        if to_view == 'y':
            print('{}\n'.format(df.drop(['month', 'hour', 'day_of_week'], axis=1).iloc[start_loc:start_loc+5]))
            start_loc += 5
        else:
            print('..skipped')
            time.sleep(1)
            break
    print('-'*44)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TODO
    # if the day, month is not all
    if df['month'].nunique() != 1:
        # display the most common month
        popular_month = df['month'].mode()[0]
        print('The month with the most trips: ', popular_month)

    if df['day_of_week'].nunique() != 1:
        # display the most common day of week
        popular_day = df['day_of_week'].mode()[0]
        print('The busiest day ', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]

    # TODO
    # print 3am / 3pm
    if popular_hour > 12:
        popular_hour -= 12
        i = 'pm'
    else:
        i = 'am'
    print('Most trips start at ', popular_hour, i)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_origin = df['Start Station'].mode()[0]
    print('Most people start their trips at: ', popular_origin)

    # display most commonly used end station
    popular_destination = df['End Station'].mode()[0]
    print('Most people end their trips at: ', popular_destination)

    # display most frequent combination of start station and end station trip
    print('Most people travel from {} to {}'.format(popular_origin, popular_destination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    start_time = time.time()

    # display total travel time
    df['Trip Duration'] = df['End Time'] - df['Start Time']
    print('The total time was: ', df['Trip Duration'].sum())

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('the mean travel time was:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    distinct_users = df['User Type'].ffill().unique()
    print('There are {} types of distinct user types:'.format(len(distinct_users)))
    for i in range(len(distinct_users)):
        print(' ', i + 1, '. ', distinct_users[i], "  ", (df['User Type'] == distinct_users[i]).sum())

    try:
        # Display counts of gender
        distinct_gender = df['Gender'].ffill().unique()
        print('\nGender break down of customers: ')
        for i in range(0, len(distinct_gender)):
            print(' ', i+1, '. ', distinct_gender[i], "  ", (df['Gender'] == distinct_gender[i]).sum())

        # Display earliest, most recent, and most common year of birth
        print('\nbirth year breakdown')
        youngest_user = df['Birth Year'].min()
        print(' Earliest: ', youngest_user)
        most_recent_user = df[df['Start Time'] == df['Start Time'].min()]
        print(' Most Recent:', most_recent_user['Birth Year'].mode()[0])
        common_yob = df['Birth Year'].mode()[0]
        print(' Most common YOB: ', common_yob)
    except KeyError:
            print('\nNo Gender or Birth Year info available')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #df = load_data('chicago', 'march', 'tuesday')

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter (y/n): ')
        if restart.lower() != 'y':
            # # TODO:
            # wish the user well
            print('Thank you for viewing, system will shutdown')
            time.sleep(3)
            print('*')
            break


if __name__ == "__main__":
    main()
