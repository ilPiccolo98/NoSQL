import constants
from detections import Detections
import pandas as pd
import matplotlib.pyplot as plt


mongodb_driver = Detections("mongodb://localhost:27017")
items = list(mongodb_driver.get_all_detections_group_by_timestamp_sum_and_avg_vehicles(constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019))
if len(items) != 0:
    data_frame = pd.DataFrame.from_records(items).set_index(["_id"])
    data_frame.plot(figsize=(20,5), color = 'blue', rot=45, title='Anderlecht', y="vehicles_avg")
    plt.show()
else:
    print("No item to show")
mongodb_driver.close()
