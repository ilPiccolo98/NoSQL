import constants
from detections import Detections
import pandas as pd
import matplotlib.pyplot as plt
from graph import Graph


mongodb_driver = Detections("mongodb://localhost:27017")
graph_detections = Graph("bolt://localhost:7687", "neo4j", "nosqlproject")
id_street = 663
min_timestamp = "2019-01-01 01:00:00"
max_timestamp = "2019-02-10 01:00:00"
items = mongodb_driver.get_detections_by_id_street(id_street, constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019)
graph_detections.remove_old_graph()
graph_detections.execute_graph_creation(items, "Anderlecht")
records, summary, keys = graph_detections.get_vehicles_filtered_by_timestamp_specific_street(min_timestamp, max_timestamp, "Anderlecht")

list_of_records = []
for record in records:
    list_of_records.append(record.data())

data_frame = pd.DataFrame.from_records(list_of_records).set_index(["timestamp"])
data_frame.plot(figsize=(20,5), color = 'red', rot=45, title='Anderlecht', kind="line")
plt.show()

records, summary, keys = graph_detections.get_average_speed_filtered_by_timestamp_specific_street(min_timestamp, max_timestamp, "Anderlecht")

list_of_records = []
for record in records:
    list_of_records.append(record.data())

data_frame = pd.DataFrame.from_records(list_of_records).set_index(["timestamp"])
data_frame.plot(figsize=(20,5), color = 'red', rot=45, title='Anderlecht', kind="line")
plt.show()

graph_detections.close()
mongodb_driver.close()
