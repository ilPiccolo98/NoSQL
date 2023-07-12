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

DF_bel_working_ = DF_and_sum[DF_and_sum['DayOfWeek'] < 5]
DF_bel_saturday_ = DF_and_sum[DF_and_sum['DayOfWeek'] == 5]
DF_bel_sunday_ = DF_and_sum[DF_and_sum['DayOfWeek'] == 6]

sns.displot(DF_and_sum['vehicles'], color = 'blue')
plt.show()
anderlecht_streets.close()
