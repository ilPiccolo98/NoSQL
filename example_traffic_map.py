import geopandas as gpd
import pandas as pd
import numpy as np
import folium
import constants
from detections import Detections
from graph_detections import Graph_detections
from traffic_map import Traffic_map

anderlecht_streets = Detections("mongodb://localhost:27017")
graph_detections = Graph_detections("bolt://localhost:7687", "neo4j", "nosqlproject")
geoJson = anderlecht_streets.get_Anderlecht_streets()
timestamp = "2019-01-25 07:40:00"
items = anderlecht_streets.get_detections_by_timestamp(timestamp, constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019)
items = list(items)
graph_detections.create_graph(items, "Anderlecht")
traffic_map = Traffic_map(geoJson, items, timestamp)
traffic_map.show()
anderlecht_streets.close()
graph_detections.close()
