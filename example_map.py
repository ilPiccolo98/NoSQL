import folium
import geopandas as gpd
from detections import Detections

mongodb_driver = Detections("mongodb://localhost:27017")
data = mongodb_driver.get_Anderlecht_streets()
data_frame = gpd.GeoDataFrame.from_features(data, data["crs"]["properties"]["name"])
street = data_frame[data_frame.index.isin([0])]
street = list(street.geometry)
#print(street[0].centroid.x, street[0].centroid.y)
polygons = data_frame
m = folium.Map([50.85045, 4.34878], zoom_start=13, tiles='cartodbpositron')
tooltip = "Click me!"
folium.Marker([street[0].centroid.y, street[0].centroid.x], popup="<i>Hey Sadas the file is here</i>", tooltip=tooltip).add_to(m)
folium.GeoJson(polygons).add_to(m)
m.show_in_browser()
mongodb_driver.close()