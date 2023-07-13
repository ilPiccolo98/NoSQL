import constants
from detections import Detections
import pandas as pd
import matplotlib.pyplot as plt


anderlecht_streets = Detections("mongodb://localhost:27017")
items = list(anderlecht_streets.get_all_detections_group_by_timestamp_sum_vehicles(constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019))
DF_and = pd.DataFrame.from_records(items).set_index(["_id"])
DF_and.plot(figsize=(20,5), color = 'red', rot=45, title='Anderlecht')
plt.show()
anderlecht_streets.close()
