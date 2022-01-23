import time
import pandas as pd
import calendar as cal

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to see data for Chicago, New York, or Washington?\n').lower()
        if city not in ['chicago', 'new york', 'washington']:
            print('Invalid input... Please try again.')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        choice = input(
            '\nWould you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n')
        if choice.lower() not in ['month', 'day', 'both', 'none']:
            print('Invalid input... Please try again.')
        else:
            if choice.lower() == 'month':
                while True:
                    month = input('\nWhich month? January, February, March, April, May, June ?\n').lower()
                    if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                        print('Invalid input... Please try again.')
                    else:
                        day = 'all'
                        break
                break

            elif choice.lower() == 'day':
                while True:
                    try:
                        day = int(input('\nWhich day? Please type you response as an integer (e.g., 1=Monday)\n')) - 1
                    except ValueError:
                        print('Invalid input... Please try again.')
                        continue

                    if day not in range(7):
                        print('Invalid input... Please try again.')
                    else:
                        month = 'all'
                        break
                break

            elif choice.lower() == 'both':
                while True:
                    month = input('\nWhich month? January, February, March, April, May, June ?\n').lower()
                    if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                        print('Invalid input... Please try again.')
                    else:
                        break
                while True:
                    try:
                        day = int(input('\nWhich day? Please type you response as an integer (e.g., 1=Monday)\n')) - 1
                    except ValueError:
                        print('Invalid input... Please try again.')
                        continue

                    if day not in range(7):
                        print('Invalid input... Please try again.')
                    else:
                        break
                break

            elif choice.lower() == 'none':
                month = 'all'
                day = 'all'
                break

    print('-' * 40)
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

    # Load the csv file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the data types of the Start Time and End Time to datatime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Getting the name of the month and the name of the day from Start time column and create 2 new columns with them
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day'] = df['Start Time'].dt.weekday

    # Filter data by the chosen month
    if month != 'all':
        df = df[df['month'] == month]

    # Filter data by the chosen day
    if day != 'all':
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    month_count = df['month'].value_counts()[0]
    print(f'Most common month: {most_common_month.title()} ... With count: {month_count}')

    # display the most common day of week
    most_common_day = cal.day_name[df['day'].mode()[0]]
    day_count = df['day'].value_counts().max()
    print(f'Most common day: {most_common_day} ... With count: {day_count}')

    # display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    start_hour_count = df['Start Time'].dt.hour.value_counts().max()
    print(f'Most common start hour: {most_common_start_hour} ... With count: {start_hour_count}')

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    start_station_count = df['Start Station'].value_counts()[0]
    print(f'Most commonly used start station: {most_common_start_station} ... With count: {start_station_count}')

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    end_station_count = df['End Station'].value_counts()[0]
    print(f'Most commonly used end station: {most_common_end_station} ... With count: {end_station_count}')

    # display most frequent combination of start station and end station trip
    most_frequent_combination = df.groupby(['Start Station', 'End Station']).size().sort_values().idxmax()
    combination_value_count = df.groupby(['Start Station', 'End Station']).size().sort_values()[-1]
    print(f'Most frequent combination of start station and end station trip are: '
          f'{most_frequent_combination[0]} and {most_frequent_combination[1]}')
    print(f'With count: {combination_value_count}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])

    s_years = total_travel_time // 31557600
    total_travel_time -= s_years * 31557600
    s_days = total_travel_time // 86400
    total_travel_time -= s_days * 86400
    s_hours = total_travel_time // 3600
    total_travel_time -= s_hours * 3600
    s_minutes = total_travel_time // 60
    total_travel_time -= s_minutes * 60
    s_seconds = total_travel_time // 1
    trips = df['Trip Duration'].shape[0]
    print(
        f'Total travel time: {int(s_years)} years,'
        f' {int(s_days)} days,'
        f' {int(s_hours)} hours,'
        f' {int(s_minutes)} minutes,'
        f' {int(s_seconds)} seconds')
    print(f'With count of: {trips} trips\n')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    m_minutes = mean_travel_time // 60
    m_seconds = mean_travel_time - (m_minutes * 60)
    print(f'Mean travel time: {m_minutes} minutes, {m_seconds} seconds')
    print(f'With count of: {trips} trips\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print(f'User types and their counts:\n{user_types_counts.to_string()}')

    # Display counts of gender
    try:
        gender_types_counts = df['Gender'].value_counts()
        print(f'\nGender Types and their counts:\n{gender_types_counts.to_string()}')
    except KeyError:
        print('\nGender types: There is no data available for this city')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_yob = df['Birth Year'].min()
        print('\nEarliest year:\n', earliest_yob)
    except KeyError:
        print('\nEarliest year: There is no data available for this city')

    try:
        most_recent_yob = df['Birth Year'].max()
        print('\nMost recent year:\n', most_recent_yob)
    except KeyError:
        print('Most recent year: There is no data available for this city')

    try:
        most_common_yob = df['Birth Year'].value_counts().idxmax()
        print('\nMost common year:\n', most_common_yob)
    except KeyError:
        print('Most common year: There is no data available for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def view_trip_data(df):
    # Filter data from month and day
    df = df.drop(['month', 'day'], axis=1)

    # Get answer from the user
    while True:
        while True:
            answer = input("\nDo you like to view individual trip data? Type 'yes' or 'no'\n")
            if answer.lower() not in ['yes', 'no']:
                print('Invalid input... Please try again.')
            else:
                start_time = time.time()
                if answer.lower() == 'yes':
                    print('Here are 5 random individuals...')
                    for i in range(5):
                        sample = df.sample().to_dict().items()
                        result = {}
                        for n in sample:
                            if n[0] == list(n[1])[0]:
                                continue
                            result[n[0]] = list(n[1].values())[0]

                        print(result)
                    print("\nThis took %s seconds." % (time.time() - start_time))
                    break
                else:
                    break

        if answer.lower() == 'no':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        view_trip_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() not in ['yes', 'no']:
                print('Invalid input... Please try again.')
            else:
                break

        if restart.lower() == 'no':
            print('We are done :) ... Thank you!')
            break


if __name__ == "__main__":
    main()
