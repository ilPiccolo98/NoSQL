import constants
from detections import Detections
from graph import Graph
from traffic_map import Traffic_map

mongodb_driver = Detections("mongodb://localhost:27017")
graph_detections = Graph("bolt://localhost:7687", "neo4j", "nosqlproject")
graph_detections.remove_old_graph()
geoJson = mongodb_driver.get_Anderlecht_streets()
timestamp = "2019-01-21 16:10:00"
items = mongodb_driver.get_detections_by_timestamp(timestamp, constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019)
graph_detections.remove_old_graph()
graph_detections.execute_graph_creation(items, "Anderlecht")

records, summary, keys = graph_detections.filter_records_by_vehicles_and_speed(5, 100, 5, 100, "Anderlecht")
list_of_records = []
for record in records:
    list_of_records.append(record.data())

if len(list_of_records) != 0:
    traffic_map = Traffic_map(geoJson, list_of_records, timestamp)
    traffic_map.show()
else:
    print("No item to plot")

mongodb_driver.close()
graph_detections.close()
