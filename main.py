import geopandas
import folium
import constants
from detections import Detections
from graph import Graph

anderlecht_streets = Detections("mongodb://localhost:27017")
graph = Graph("bolt://localhost:7687", "neo4j", "nosqlproject")
items = anderlecht_streets.get_data(constants.anderlecht, constants.granularity_05min, constants.range_01_03_2019)
graph.execute_query("MATCH (n) DELETE n")
for item in items.limit(5):
    graph.execute_query("CREATE (n:STREET {id_street: %f})" % item["id_street"])
anderlecht_streets.close()
graph.close()


'''
anderlecht = geopandas.read_file('../dataset/Anderlecht_streets.json')
print('Anderlecht total number of streets '+str(anderlecht.shape[0]))


polygons = anderlecht
m = folium.Map([50.85045, 4.34878], zoom_start=13, tiles='cartodbpositron')
folium.GeoJson(polygons).add_to(m)
m.show_in_browser()
'''
