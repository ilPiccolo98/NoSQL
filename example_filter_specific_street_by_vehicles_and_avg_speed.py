import constants
from detections import Detections
import pandas as pd
import matplotlib.pyplot as plt
from graph import Graph


mongodb_driver = Detections("mongodb://localhost:27017")
graph_detections = Graph("bolt://localhost:7687", "neo4j", "nosqlproject")
id_street = 663
min_vehicles = 20
max_vehicles = 50
items = mongodb_driver.get_detections_by_id_street(id_street, constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019)
graph_detections.remove_old_graph()
graph_detections.execute_graph_creation(items, "Anderlecht")
records, summary, keys = graph_detections.get_timestamps_filtered_by_min_and_max_vehicles(min_vehicles, max_vehicles, "Anderlecht")

list_of_records = []
for record in records:
    list_of_records.append(record.data())

if len(list_of_records) != 0:
    data_frame = pd.DataFrame.from_records(list_of_records).set_index(["timestamp"])
    data_frame.plot(figsize=(20,5), color = 'red', rot=45, title='Anderlecht', kind="line")
    plt.show()
else:
    print("No item to plot")

min_avg_speed = 40
max_avg_speed = 70
records, summary, keys = graph_detections.get_timestamps_filtered_by_min_and_max_avg_speed(min_avg_speed, max_avg_speed, "Anderlecht")

list_of_records = []
for record in records:
    list_of_records.append(record.data())

if len(list_of_records) != 0:
    data_frame = pd.DataFrame.from_records(list_of_records).set_index(["timestamp"])
    data_frame.plot(figsize=(20,5), color = 'red', rot=45, title='Anderlecht', kind="line")
    plt.show()
else:
    print("No item to plot")

graph_detections.close()
mongodb_driver.close()
