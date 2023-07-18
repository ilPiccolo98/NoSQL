import geopandas as gpd
import pandas as pd
import numpy as np
import folium
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
list_of_items = list(items)
graph_detections.remove_old_graph()
graph_detections.execute_graph_creation(list_of_items, "Anderlecht")
if len(list_of_items) != 0:
    traffic_map = Traffic_map(geoJson, list_of_items, timestamp)
else:
    print("No item to plot")
traffic_map.show()
mongodb_driver.close()
graph_detections.close()
