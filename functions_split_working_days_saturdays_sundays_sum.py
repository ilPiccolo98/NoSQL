import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

def init_functions_split_working_days_saturdays_sundays_sum(items):
    if len(items) != 0:
        data_frame = pd.DataFrame.from_records(items)

        data_frame['time'] = pd.to_datetime(data_frame['_id']).dt.time
        data_frame['DayOfWeek'] = pd.to_datetime(data_frame['_id']).dt.dayofweek

        data_frame_working_ = data_frame[data_frame['DayOfWeek'] < 5]
        data_frame_saturday_ = data_frame[data_frame['DayOfWeek'] == 5]
        data_frame_sunday_ = data_frame[data_frame['DayOfWeek'] == 6]

        return data_frame, data_frame_working_, data_frame_saturday_, data_frame_sunday_
    else:
        print("No item to plot")


# Count trucks: split working days, saturdays and sundays

def total_distributions(data_frame):
    sns.distplot(data_frame['vehicles_sum'], hist=False, kde=True,
                bins= 200, color = 'blue',
                hist_kws={'edgecolor':'black'})
    plt.show()


def working_days_distribution(data_frame_working_):
    sns.distplot(data_frame_working_['vehicles_sum'], hist=False, kde=True,
                bins= 200, color = 'blue',
                hist_kws={'edgecolor':'black'})
    plt.show()


def working_days_day_night_distribution(data_frame_working_):
    start = datetime.strptime('03:00:00', '%H:%M:%S').time()
    end = datetime.strptime('15:00:00', '%H:%M:%S').time()

    data_frame_working_day = data_frame_working_[data_frame_working_['time'].between(start, end)]

    start = datetime.strptime('15:00:00', '%H:%M:%S').time()
    middle_1 = datetime.strptime('23:59:00', '%H:%M:%S').time()
    middle_2 = datetime.strptime('00:00:00', '%H:%M:%S').time()
    end = datetime.strptime('02:59:00', '%H:%M:%S').time()

    data_frame_working_night_1 = data_frame_working_[data_frame_working_['time'].between(start, middle_1)]
    data_frame_working_night_2 = data_frame_working_[data_frame_working_['time'].between(middle_2, end)]

    data_frame_working_night = pd.concat([data_frame_working_night_1, data_frame_working_night_2], axis=0)

    sns.distplot(data_frame_working_day['vehicles_sum'], hist=False, kde=True,
                bins= 200, color = 'blue',
                hist_kws={'edgecolor':'black'})
    plt.show()

    sns.distplot(data_frame_working_night['vehicles_sum'], hist=False, kde=True,
                bins= 200, color = 'blue',
                hist_kws={'edgecolor':'black'})
    plt.show()


def saturdays_distribution(data_frame_saturday_):
    sns.distplot(data_frame_saturday_['vehicles_sum'], hist=False, kde=True,
                bins= 200, color = 'blue',
                hist_kws={'edgecolor':'black'})
    plt.show()


def sundays_distribution(data_frame_sunday_):
    sns.distplot(data_frame_sunday_['vehicles_sum'], hist=False, kde=True,
                bins= 200, color = 'blue',
                hist_kws={'edgecolor':'black'})
    plt.show()



#   Visualise average daily pattern

def average_daily_pattern_working_days(data_frame_working_):
    data_frame_working = data_frame_working_.groupby('time').agg({'vehicles_sum':['mean']})
    data_frame_working.columns = ['mean']
    ax = data_frame_working[['mean']].plot(color="orange", title = 'avg working days daily pattern')
    plt.show()


def average_daily_pattern_saturday_days(data_frame_saturday_):
    data_frame_saturday = data_frame_saturday_.groupby('time').agg({'vehicles_sum':['mean']})
    data_frame_saturday.columns = ['mean']
    ax = data_frame_saturday[['mean']].plot(color="orange", title = 'avg saturdays daily pattern')
    plt.show()


def average_daily_pattern_sunday_days(data_frame_sunday_):
    data_frame_sunday = data_frame_sunday_.groupby('time').agg({'vehicles_sum':['mean']})
    data_frame_sunday.columns = ['mean']
    ax = data_frame_sunday[['mean']].plot(color="orange", title = 'avg sundays daily pattern')
    plt.show()


def average_daily_pattern_all_together(data_frame_working_, data_frame_saturday_, data_frame_sunday_):
    data_frame_working = data_frame_working_.groupby('time').agg({'vehicles_sum':['mean']})
    data_frame_working.columns = ['mean']

    data_frame_saturday = data_frame_saturday_.groupby('time').agg({'vehicles_sum':['mean']})
    data_frame_saturday.columns = ['mean']

    data_frame_sunday = data_frame_sunday_.groupby('time').agg({'vehicles_sum':['mean']})
    data_frame_sunday.columns = ['mean']

    data_frame_working['avg working days'] = data_frame_working[['mean']]
    data_frame_saturday['avg saturdays'] = data_frame_saturday[['mean']]
    data_frame_sunday['avg sunday'] = data_frame_sunday[['mean']]
    ax = data_frame_working[['avg working days']].plot(color="red", title = 'avg  day pattern')
    data_frame_saturday[['avg saturdays']].plot(ax=ax, color="green")
    data_frame_sunday[['avg sunday']].plot(ax=ax, color="blue")
    plt.show()
