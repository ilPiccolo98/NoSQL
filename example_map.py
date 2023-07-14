import folium
from folium import features
import geopandas as gpd
from detections import Detections

mongodb_driver = Detections("mongodb://localhost:27017")
data = mongodb_driver.get_Anderlecht_streets()
data_frame = gpd.GeoDataFrame.from_features(data, data["crs"]["properties"]["name"])
ids = list(range(data_frame.size))
data_frame["id"] = ids
m = folium.Map([50.85045, 4.34878], zoom_start=13, tiles='cartodbpositron')
features.GeoJson(data_frame, name='Labels', tooltip=features.GeoJsonTooltip(fields=['id'],
                                                                            aliases = ['Street id'],
                                                                            labels=True,
                                                                            sticky=False)).add_to(m)
m.show_in_browser()
mongodb_driver.close()