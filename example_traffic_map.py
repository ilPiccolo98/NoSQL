import geopandas as gpd
import pandas as pd
import numpy as np
import folium
import constants
from detections import Detections
from graph import Graph
from traffic_map import Traffic_map

anderlecht_streets = Detections("mongodb://localhost:27017")
graph_detections = Graph("bolt://localhost:7687", "neo4j", "nosqlproject")
graph_detections.remove_old_graph()
geoJson = anderlecht_streets.get_Anderlecht_streets()
timestamp = "2019-01-25 07:40:00"
items = anderlecht_streets.get_detections_by_timestamp(timestamp, constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019)
list_of_items = list(items)
graph_detections.execute_graph_creation(items, "Anderlecht")
traffic_map = Traffic_map(geoJson, list_of_items, timestamp)
traffic_map.show()
anderlecht_streets.close()
graph_detections.close()
