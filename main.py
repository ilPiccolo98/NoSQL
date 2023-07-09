import geopandas
import folium
import constants
from detections import Detections
from graph_detections import Graph_detections

anderlecht_streets = Detections("mongodb://localhost:27017")
graph_detections = Graph_detections("bolt://localhost:7687", "neo4j", "nosqlproject")
items = anderlecht_streets.get_detections_by_timestamp("2019-01-04 10:20:00", constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019)
graph_detections.create_graph(list(items), "Anderlecht")
anderlecht_streets.close()
graph_detections.close()


'''
anderlecht = geopandas.read_file('../dataset/Anderlecht_streets.json')
print('Anderlecht total number of streets '+str(anderlecht.shape[0]))


polygons = anderlecht
m = folium.Map([50.85045, 4.34878], zoom_start=13, tiles='cartodbpositron')
folium.GeoJson(polygons).add_to(m)
m.show_in_browser()
'''
