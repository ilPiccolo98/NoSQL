import folium
import geopandas as gpd

df_anderlecht = gpd.read_file('../dataset/Anderlecht_streets.json')
street = df_anderlecht[df_anderlecht.index.isin([0])]
street = list(street.geometry)
print(street[0].centroid.x, street[0].centroid.y)
polygons = df_anderlecht
m = folium.Map([50.85045, 4.34878], zoom_start=13, tiles='cartodbpositron')
tooltip = "Click me!"
folium.Marker([street[0].centroid.y, street[0].centroid.x], popup="<i>Hey Sadas the file is here</i>", tooltip=tooltip).add_to(m)
folium.GeoJson(polygons).add_to(m)
m.show_in_browser()