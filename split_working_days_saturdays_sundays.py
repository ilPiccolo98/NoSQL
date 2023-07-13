import constants
from detections import Detections
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

anderlecht_streets = Detections("mongodb://localhost:27017")
items = list(anderlecht_streets.get_all_detections(constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019))
DF_and = pd.DataFrame.from_records(items)


DF_and_sum = DF_and.sort_values(by=['timestamp']).groupby(['timestamp']).agg({'vehicles':'sum'}).reset_index()
DF_and_sum['time'] = pd.to_datetime(DF_and_sum['timestamp']).dt.time
DF_and_sum['DayOfWeek'] = pd.to_datetime(DF_and_sum['timestamp']).dt.dayofweek

DF_and_working_ = DF_and_sum[DF_and_sum['DayOfWeek'] < 5]
DF_and_saturday_ = DF_and_sum[DF_and_sum['DayOfWeek'] == 5]
DF_and_sunday_ = DF_and_sum[DF_and_sum['DayOfWeek'] == 6]

sns.distplot(DF_and_sum['vehicles'], hist=False, kde=True, 
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

anderlecht_streets.close()
