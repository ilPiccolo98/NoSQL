import geopandas as gpd
import pandas as pd
import numpy as np
import folium
import constants
from detections import Detections
from graph import Graph


anderlecht_streets = Detections("mongodb://localhost:27017")
graph = Graph("bolt://localhost:7687", "neo4j", "nosqlproject")
graph.remove_old_graph()
items = anderlecht_streets.get_detections_by_timestamp("2019-01-04 10:20:00", constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019)
graph.execute_graph_creation(items, "Anderlecht")
anderlecht_streets.close()
graph.close()
