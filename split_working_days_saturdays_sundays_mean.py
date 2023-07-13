import constants
from detections import Detections
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

anderlecht_streets = Detections("mongodb://localhost:27017")
items = list(anderlecht_streets.get_all_detections_group_by_timestamp_avg_vehicles(constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019))
DF_and = pd.DataFrame.from_records(items)


DF_and['time'] = pd.to_datetime(DF_and['_id']).dt.time
DF_and['DayOfWeek'] = pd.to_datetime(DF_and['_id']).dt.dayofweek

DF_and_working_ = DF_and[DF_and['DayOfWeek'] < 5]
DF_and_saturday_ = DF_and[DF_and['DayOfWeek'] == 5]
DF_and_sunday_ = DF_and[DF_and['DayOfWeek'] == 6]

sns.distplot(DF_and['vehicles'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()
sns.distplot(DF_and_working_['vehicles'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()
sns.distplot(DF_and_saturday_['vehicles'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()
sns.distplot(DF_and_sunday_['vehicles'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()


start = datetime.strptime('03:00:00', '%H:%M:%S').time()
end = datetime.strptime('15:00:00', '%H:%M:%S').time()

DF_bel_working_day = DF_and_working_[DF_and_working_['time'].between(start, end)]


start = datetime.strptime('15:00:00', '%H:%M:%S').time()
middle_1 = datetime.strptime('23:59:00', '%H:%M:%S').time()
middle_2 = datetime.strptime('00:00:00', '%H:%M:%S').time()
end = datetime.strptime('02:59:00', '%H:%M:%S').time()

DF_bel_working_night_1 = DF_and_working_[DF_and_working_['time'].between(start, middle_1)]
DF_bel_working_night_2 = DF_and_working_[DF_and_working_['time'].between(middle_2, end)]

DF_bel_working_night = pd.concat([DF_bel_working_night_1, DF_bel_working_night_2], axis=0)

sns.distplot(DF_bel_working_day['vehicles'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()


sns.distplot(DF_bel_working_night['vehicles'], hist=False, kde=True, 
             bins= 200, color = 'blue',
             hist_kws={'edgecolor':'black'})
plt.show()

anderlecht_streets.close()
