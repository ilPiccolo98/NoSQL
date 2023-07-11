import folium
import geopandas as gpd
import branca.colormap as cm

class Traffic_map:
    def __init__(self, geoJson, data, timestamp):
        self.__timestamp = timestamp
        data = sorted(data, key=self.__sort_by_id_streets)
        streets = self.__get_streets(data)
        geoJsonFiltered = self.__filter_geoJson_by_id_streets(geoJson, streets)
        self.__geoData = gpd.GeoDataFrame.from_features(geoJsonFiltered, geoJsonFiltered["crs"]["properties"]["name"])
        self.__geoData["Vehicles_Flow"] = self.__get_vehicles(data)

    def show(self):
        colormap_dept = cm.StepColormap(colors=['#00ae53', '#ffe6a4', '#ee0028'],
                                                vmin = 0,
                                                vmax = 100,
                                                index=[0, 20, 50, 100])
        polygons = self.__geoData
        m = folium.Map([50.85045, 4.34878], zoom_start= 9, tiles='cartodbpositron')
        style_function = lambda x: { 'fillColor': colormap_dept(x['properties']['Vehicles_Flow']),
                                     'color': colormap_dept(x['properties']['Vehicles_Flow']),
                                     'weight': 1.5,
                                     'fillOpacity': 1}
        folium.GeoJson(polygons, style_function=style_function).add_to(m)
        colormap_dept.caption = 'Traffic Flow - Timestamp: %s' % self.__timestamp
        colormap_dept.add_to(m)
        m.show_in_browser()

    def __sort_by_id_streets(self, item):
        return item["id_street"]
    
    def __get_streets(self, items):
        id_streets = []
        for item in items:
            id_streets.append(item["id_street"])
        return id_streets
    
    def __get_vehicles(self, items):
        vehicles = []
        for item in items:
            vehicles.append(item["vehicles"])
        return vehicles
    
    def __filter_geoJson_by_id_streets(self, geoJson, streets):
        streets_to_store = []
        for street in streets:
            streets_to_store.append(geoJson["features"][int(street)])
        geoJsonFiltered = geoJson.copy()
        geoJsonFiltered["features"] = streets_to_store
        return geoJsonFiltered
    