import constants
from detections import Detections
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

mongodb_driver = Detections("mongodb://localhost:27017")
items = list(mongodb_driver.get_all_detections_group_by_timestamp_sum_and_avg_vehicles(constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019))
data_frame = pd.DataFrame.from_records(items)


data_frame['time'] = pd.to_datetime(data_frame['_id']).dt.time
data_frame['DayOfWeek'] = pd.to_datetime(data_frame['_id']).dt.dayofweek

data_frame_working_ = data_frame[data_frame['DayOfWeek'] < 5]
data_frame_saturday_ = data_frame[data_frame['DayOfWeek'] == 5]
data_frame_sunday_ = data_frame[data_frame['DayOfWeek'] == 6]

sns.distplot(data_frame['vehicles_avg'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()
sns.distplot(data_frame_working_['vehicles_avg'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()
sns.distplot(data_frame_saturday_['vehicles_avg'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()
sns.distplot(data_frame_sunday_['vehicles_avg'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()


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

sns.distplot(data_frame_working_day['vehicles_avg'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()


sns.distplot(data_frame_working_night['vehicles_avg'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()

mongodb_driver.close()
