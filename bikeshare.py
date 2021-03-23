import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = str(input("Would you like to see data for Chicago, New York, or washington ?"))
    if city.lower() not in list(CITY_DATA.keys()) and city.lower() not in ["new york", "New York"]:
        city = str(input("Please enter a valid city"))
    elif city == "New York" or city == "new york":
        city += " city"

    # get user input for month (all, jan, feb, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    time_filter = str(input("Would you like to filter data with month, day, or both? Please enter none for no time filters"))
    month = None
    day = None
    if time_filter == "month":
        month = str(input("Which month would you want to filter with ? [all, jan, feb, mar, apr, may, june]"))
        day = "all"
    elif time_filter == "day":
        day = str(input("Which day would you want to filter with ? [all, Monday, Tuesday, Wednesday, Thursdat, Friday, Satureday, Sunday ]"))
        month = "all"
    elif time_filter == "both":
        month = str(input("Which month would you want to filter with ? [all, Jan, Feb, Mar, Apr, May, June]"))
        day = str(input("Which day would you want to filter with ? [all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday ]"))
    elif time_filter == "none":
        month = None
        day = None
    else:
        print("please enter a valid input")
        get_filters()



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
    data_file = pd.read_csv(CITY_DATA[city])
    data_file["Start Time"] = pd.to_datetime(data_file["Start Time"], format = "%Y-%m-%d %H:%M:%S")
    data_file["month"] = data_file["Start Time"].dt.strftime("%b")
    data_file["Start Hour"] = data_file["Start Time"].dt.hour
    data_file["Day"] = data_file["Start Time"].dt.strftime("%A")
    days = ["SaturDay", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June"]
    if month.capitalize() in months:
        df = data_file[data_file["month"] == month.capitalize()]
    else:
        df = data_file
    if day in days:
        df = df[df["Day"] == day]
    else:
        df = df
    return df


def time_stats(df, filter1):
    """Displays statistics on the most frequent times of travel."""
    # display the most common month
    # display the most common day of week
    # display the most common start hour
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # if we filter with both then we have to calculate the nos common hour only
    if filter1 == "both":
        popular_hour = df["Start Hour"].mode()[0]
        popular_hour_count = max(df.groupby(["Start Hour"])["Start Hour"].count())
        print("Most popular Hour: {}, Count: {}".format(popular_hour, popular_hour_count))
        print("filter:",filter1)
    
    # if we filter with month then we have to calculate the most common day and most common hour
    elif filter1 == "month":
        popular_day = df["Day"].mode()[0]
        popular_day_count = max(df.groupby(["Day"])["Day"].count())
        popular_hour = df["Start Hour"].mode()[0]
        popular_hour_count = max(df.groupby(["Start Hour"])["Start Hour"].count())
        print("Most popular day of week: {} count: {}".format(popular_day, popular_day_count))
        print("Most popular hour:{}, Count: {}".format( popular_hour, popular_hour_count))
        print("Filter: ", filter1)
    
    #if we filter with day then we have to calcuate the most common month and the monst common hour
    elif filter1 == "day":
        popular_month = df["month"].mode()[0]
        popular_month_count = max(df.groupby(["month"])["month"].count())
        popular_hour = df["Start Hour"].mode()[0]
        popular_hour_count = max(df.groupby(["Start Hour"])["Start Hour"].count())
        print("Most popular month: {}, Count: {}".format(popular_month, popular_month_count))
        print("Most popular hour:{}, Count: {}".format(popular_hour, popular_hour_count))
        print("filter:",filter1)
    # if we don't have any filter then we have to calculate Most common month, day and hour
    else: 
        popular_month = df["month"].mode()[0]
        popular_month_count = max(df.groupby(["month"])["month"].count())
        popular_day = df["Day"].mode()[0]
        popular_day_count = max(df.groupby(["Day"])["Day"].count())
        popular_hour = df["Start Hour"].mode()[0]
        popular_hour_count = max(df.groupby(["Start Hour"])["Start Hour"].count())
        print("Most popular monht: {}, Count: {}".format(popular_month, popular_month_count))
        print("Most popular hour:{}, Count: {}".format(popular_hour, popular_hour_count))
        print("filter:",filter1)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, filter1):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df["Start Station"].mode()[0]
    common_start_count = max(df.groupby(["Start Station"])["Start Station"].count())   

    # display most commonly used end station
    common_end = df["End Station"].mode()[0]
    common_end_count = max(df.groupby(["End Station"])["End Station"].count())

    # display most frequent combination of start station and end station trip
    df["Common Trip"] = df["Start Station"]+", "+df["End Station"]
    common_trip = df["Common Trip"].mode()[0]
    common_trip_count = max(df.groupby(["Common Trip"])["Common Trip"].count())

    #----- Output Foramatting ------#
    print("Common Start Station :",common_start,", Count:",common_start_count)
    print("Common End Station:",common_end,", Count:",common_end_count)
    print("filter:",filter1)
    print("Trip:", "('", common_trip.split(", ")[0], "', '", common_trip.split(", ")[1], "'), Count:",common_trip_count)
    print("filter:",filter1)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, filter1):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # caculating total travel time
    total_trip = df["Trip Duration"].sum()
    # Caculating mean travel time
    average_trip = df["Trip Duration"].mean()
    # Clacuating count
    trip_count = df["Trip Duration"].count()

    ### Output formatting ####
    print("Total trip duration: ",total_trip,", Average trip duration: ", average_trip,", Count: ", trip_count)
    print("Filter: ",filter1)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, filter1):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df["User Type"].value_counts()
    print("Subscribers: ", user_type_counts[0],", Customers: ", user_type_counts[1], "Filter: ", filter1)
    # Display counts of gender
    if "Gender" in df.columns:
        gender_counts = df["Gender"].value_counts()
        print("Male: ",gender_counts[0],",Female: ",gender_counts[1])
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        most_recent_birth = df["Birth Year"].max()
        earliest_birth = df["Birth Year"].min()
        most_common_birth = df["Birth Year"].mode()[0]
        print("Most recent year of birth: ",most_recent_birth, ", Earliest year of birth: ",earliest_birth,", Most common year of birth: ", most_common_birth, "Filter: ", filter1)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# New function to get ask the user if we want to display some rows
def DisplayRawData(df):
    i = 0
    while(True):
        display_data = str(input("Do you want to display 5 lines of raw data? [yes] or [no]"))
        if display_data == "yes":
            end = i+5
            print(df.iloc[i:end, :-4])
            i +=5
        elif display_data == "no":
            break



def main():
    while True:
        city, month, day = get_filters()
        ##### Handling the none input########
        if month == None:
            month ="all"
        if day == None:
            day == "all"
        ######################################
        df = load_data(city, month, day)
        ### Determine the filter type #############################
        filter1 = "all"
        if month not in ["all", None] and day not in ["all", None]:
            filter1 = "both"
        elif month not in ["all", None] and day in ["all", None]:
            filter1 = "month"
        elif month in ["all", None] and day not in ["all", None]:
            filter1 = "day"
        ##############################################################
        time_stats(df, filter1)
        station_stats(df, filter1)
        trip_duration_stats(df, filter1)
        user_stats(df, filter1)
        DisplayRawData(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()