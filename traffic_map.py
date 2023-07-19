import folium
import geopandas as gpd
import branca.colormap as cm
from folium import features

class Traffic_map:
    def __init__(self, geoJson, data, timestamp):
        self.__timestamp = timestamp
        streets, vehicles, avg_speed = self._get_list_of_properties(data)
        geoJsonFiltered = self.__filter_geoJson_by_id_streets(geoJson, streets)
        self.__geoData = gpd.GeoDataFrame.from_features(geoJsonFiltered, geoJsonFiltered["crs"]["properties"]["name"])
        self.__geoData["Vehicles"] = vehicles
        self.__geoData["Id street"] = streets
        self.__geoData["Average speed"] = avg_speed

    def show(self):
        colormap_dept = cm.StepColormap(colors=['#00ae53', '#86dc76', '#daf8aa', 
                                                '#ffe6a4', '#ff9a61', '#ee0028'],
                                        vmin = 0,
                                        vmax = 200,
                                        index=[0, 20, 50, 80, 110, 150, 180])
        polygons = self.__geoData
        m = folium.Map([50.85045, 4.34878], zoom_start= 9, tiles='cartodbpositron')
        style_function = lambda x: { 'fillColor': colormap_dept(x['properties']['Vehicles']),
                                     'color': colormap_dept(x['properties']['Vehicles']),
                                     'weight': 1.5,
                                     'fillOpacity': 1}
        folium.GeoJson(polygons, style_function=style_function, tooltip=features.GeoJsonTooltip(fields=['Id street', "Vehicles", "Average speed"],
                                                                            aliases = ['Street id', "Vehicles", "Average speed"],
                                                                            labels=True,
                                                                            sticky=False)).add_to(m)
        colormap_dept.caption = 'Traffic Flow - Timestamp: %s' % self.__timestamp
        colormap_dept.add_to(m)
        return m
    
    def _get_list_of_properties(self, items):
        id_streets = []
        vehicles = []
        avg_speed = []
        for item in items:
            id_streets.append(item["id_street"])
            vehicles.append(item["vehicles"])
            avg_speed.append(item["average_speed"])
        return id_streets, vehicles, avg_speed
    
    def __filter_geoJson_by_id_streets(self, geoJson, streets):
        streets_to_store = []
        for street in streets:
            streets_to_store.append(geoJson["features"][int(street)])
        geoJsonFiltered = {}
        geoJsonFiltered["type"] = geoJson["type"]
        geoJsonFiltered["crs"] = geoJson["crs"]
        geoJsonFiltered["features"] = streets_to_store
        return geoJsonFiltered
    