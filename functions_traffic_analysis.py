import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import features
import geopandas as gpd

import constants
from traffic_map import Traffic_map


# Traffico del dataset selezionato rappresentato come somma dei veicoli per ciascuna strada
def traffic_sum_vehicles_for_street(items, rete_stradale):
    if len(items) != 0:
        data_frame = pd.DataFrame.from_records(items).set_index(["_id"])
        if rete_stradale == constants.anderlecht:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Anderlecht')
        elif rete_stradale == constants.bruxells:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Bruxelles')
        elif rete_stradale == constants.belgium:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Belgium')

        plt.show()
    else:
        print("No items to show")


# Traffico del dataset selezionato rappresentato come media dei veicoli per ciascuna strada
def traffic_avg_vehicles_for_street(items, rete_stradale):
    if len(items) != 0:
        data_frame = pd.DataFrame.from_records(items).set_index(["_id"])
        if rete_stradale == constants.anderlecht:
            data_frame.plot(figsize=(20, 5), color='blue', rot=45, title='Anderlecht', y="vehicles_avg")
        elif rete_stradale == constants.bruxells:
            data_frame.plot(figsize=(20, 5), color='blue', rot=45, title='Bruxelles', y="vehicles_avg")
        elif rete_stradale == constants.belgium:
            data_frame.plot(figsize=(20, 5), color='blue', rot=45, title='Belgium', y="vehicles_avg")

        plt.show()
    else:
        print("No item to show")


# Mostra le strade di una citta'
def show_street_of_city(mongodb_driver, rete_stradale):
    if rete_stradale == constants.anderlecht:
        data = mongodb_driver.get_Anderlecht_streets()
    elif rete_stradale == constants.bruxells:
        data = mongodb_driver.get_Bruxelles_streets()
    elif rete_stradale == constants.belgium:
        data = mongodb_driver.get_Belgium_streets()

    data_frame = gpd.GeoDataFrame.from_features(data, data["crs"]["properties"]["name"])
    ids = list(range(data_frame.size))
    data_frame["id"] = ids
    m = folium.Map([50.85045, 4.34878], zoom_start=13, tiles='cartodbpositron')
    features.GeoJson(data_frame, name='Labels', tooltip=features.GeoJsonTooltip(fields=['id'],
                                                                                aliases = ['Street id'],
                                                                                labels=True,
                                                                                sticky=False)).add_to(m)
    return m


# Traffico delle strade ad un istante di tempo
def traffic_city_at_specific_time(mongodb_driver, graph_detections, rete_stradale, risoluzione_temporale, periodo_tempo):
    graph_detections.remove_old_graph()
    if rete_stradale == constants.anderlecht:
        geoJson = mongodb_driver.get_Anderlecht_streets()
    elif rete_stradale == constants.bruxells:
        geoJson = mongodb_driver.get_Bruxelles_streets()
    elif rete_stradale == constants.belgium:
        geoJson = mongodb_driver.get_Belgium_streets()

    anno = input("Inserisci un istante di tempo nel seguente formato AAAA-MM-GG ORA:MIN:\n"
                 "Nota. Valori possibili per Anno: " + periodo_tempo[10:] + "\n"
                                                                            "Anno AAAA:")
    mese = input("Nota. Valori possibili per Mese: da " + periodo_tempo[2:4] + " a " + periodo_tempo[7:9] + "\n"
                                                                                                            "Mese MM:")
    giorno = input("Giorno GG:")
    ora = input("Ora 24H (da 00 a 23):")
    minuti = input("Minuti (da 00 a 55. Nota: devono essere multipli di " + risoluzione_temporale + "):")
    secondi = "00"
    timestamp = anno + "-" + mese + "-" + giorno + " " + ora + ":" + minuti + ":" + secondi

    items = mongodb_driver.get_detections_by_timestamp(timestamp, rete_stradale, risoluzione_temporale, periodo_tempo)
    list_of_items = list(items)
    graph_detections.remove_old_graph()

    if rete_stradale == constants.anderlecht:
        graph_detections.execute_graph_creation(list_of_items, "Anderlecht")
    elif rete_stradale == constants.bruxells:
        graph_detections.execute_graph_creation(list_of_items, "Bruxelles")
    elif rete_stradale == constants.belgium:
        graph_detections.execute_graph_creation(list_of_items, "Belgium")

    if len(list_of_items) != 0:
        traffic_map = Traffic_map(geoJson, list_of_items, timestamp)
    else:
        print("No item to plot")

    m = traffic_map.show()
    return m


# Traffico delle strade ad un istante di tempo, filtrando anche per numero di veicoli e per la velocita' media
def traffic_city_at_specific_time_filter_by_number_vehicles_avg_speed(mongodb_driver, graph_detections, rete_stradale, risoluzione_temporale, periodo_tempo):
    graph_detections.remove_old_graph()
    if rete_stradale == constants.anderlecht:
        geoJson = mongodb_driver.get_Anderlecht_streets()
    elif rete_stradale == constants.bruxells:
        geoJson = mongodb_driver.get_Bruxelles_streets()
    elif rete_stradale == constants.belgium:
        geoJson = mongodb_driver.get_Belgium_streets()

    anno = input("Inserisci un istante di tempo nel seguente formato AAAA-MM-GG ORA:MIN:\n"
                 "Nota. Valori possibili per Anno: " + periodo_tempo[10:] + "\n"
                                                                            "Anno AAAA:")
    mese = input("Nota. Valori possibili per Mese: da " + periodo_tempo[2:4] + " a " + periodo_tempo[7:9] + "\n"
                                                                                                            "Mese MM:")
    giorno = input("Giorno GG:")
    ora = input("Ora 24H (da 00 a 23):")
    minuti = input("Minuti (da 00 a 55. Nota: devono essere multipli di " + risoluzione_temporale + "):")
    secondi = "00"
    timestamp = anno + "-" + mese + "-" + giorno + " " + ora + ":" + minuti + ":" + secondi

    items = mongodb_driver.get_detections_by_timestamp(timestamp, rete_stradale, risoluzione_temporale, periodo_tempo)
    graph_detections.remove_old_graph()

    if rete_stradale == constants.anderlecht:
        graph_detections.execute_graph_creation(items, "Anderlecht")
        city = "Anderlecht"
    elif rete_stradale == constants.bruxells:
        graph_detections.execute_graph_creation(items, "Bruxelles")
        city = "Bruxelles"
    elif rete_stradale == constants.belgium:
        graph_detections.execute_graph_creation(items, "Belgium")
        city = "Belgium"

    min_speed = int(input("Inserisci i seguenti valori:"
                          "+ Velocita' minima:"))
    max_speed = int(input("+ Velocita' massima:"))
    min_mean_speed = int(input("+ Velocita' media minima:"))
    max_mean_speed = int(input("+ Velocita' media massima:"))
    records, summary, keys = graph_detections.filter_records_by_vehicles_and_speed(min_speed, max_speed, min_mean_speed, max_mean_speed, city)
    list_of_records = []
    for record in records:
        list_of_records.append(record.data())

    if len(list_of_records) != 0:
        traffic_map = Traffic_map(geoJson, list_of_records, timestamp)
        m = traffic_map.show()
        return m
    else:
        print("No item to plot")


# Mostrare la velocita' media e il traffico di una strada in uno specifico intervallo di tempo
def traffic_avg_speed_street_at_specific_timerange(mongodb_driver, graph_detections, rete_stradale, risoluzione_temporale, periodo_tempo):

    id_street = int(input("Inserisci l'id della strada"))

    anno_min = input("Inserisci un istante di tempo nel seguente formato AAAA-MM-GG ORA:MIN:\n"
                 "Nota. Valori possibili per Anno: " + periodo_tempo[10:] + "\n"
                                                                            "Anno AAAA:")
    mese_min = input("Nota. Valori possibili per Mese: da " + periodo_tempo[2:4] + " a " + periodo_tempo[7:9] + "\n"
                                                                                                            "Mese MM:")
    giorno_min = input("Giorno GG:")
    ora_min = input("Ora 24H (da 00 a 23):")
    minuti_min = input("Minuti (da 00 a 55. Nota: devono essere multipli di " + risoluzione_temporale + "):")
    secondi = "00"
    min_timestamp = anno_min + "-" + mese_min + "-" + giorno_min + " " + ora_min + ":" + minuti_min + ":" + secondi
    print("MIN TIMESTAMP: ", min_timestamp)

    anno_max = input("Inserisci un istante di tempo nel seguente formato AAAA-MM-GG ORA:MIN:\n"
                 "Nota. Valori possibili per Anno: " + periodo_tempo[10:] + "\n"
                                                                            "Anno AAAA:")
    mese_max = input("Nota. Valori possibili per Mese: da " + periodo_tempo[2:4] + " a " + periodo_tempo[7:9] + "\n"
                                                                                                            "Mese MM:")
    giorno_max = input("Giorno GG:")
    ora_max = input("Ora 24H (da 00 a 23):")
    minuti_max = input("Minuti (da 00 a 55. Nota: devono essere multipli di " + risoluzione_temporale + "):")
    secondi = "00"
    max_timestamp = anno_max + "-" + mese_max + "-" + giorno_max + " " + ora_max + ":" + minuti_max + ":" + secondi
    print("MAX TIMESTAMP: ", max_timestamp)

    items = mongodb_driver.get_detections_by_id_street(id_street, rete_stradale, risoluzione_temporale, periodo_tempo)
    graph_detections.remove_old_graph()

    if rete_stradale == constants.anderlecht:
        graph_detections.execute_graph_creation(items, "Anderlecht")
        city = "Anderlecht"
    elif rete_stradale == constants.bruxells:
        graph_detections.execute_graph_creation(items, "Bruxelles")
        city = "Bruxelles"
    elif rete_stradale == constants.belgium:
        graph_detections.execute_graph_creation(items, "Belgium")
        city = "Belgium"

    records, summary, keys = graph_detections.get_vehicles_filtered_by_timestamp_specific_street(min_timestamp,
                                                                                                 max_timestamp,
                                                                                                 city)
    list_of_records = []
    for record in records:
        list_of_records.append(record.data())

    if len(list_of_records) != 0:
        data_frame = pd.DataFrame.from_records(list_of_records).set_index(["timestamp"])

        if rete_stradale == constants.anderlecht:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Anderlecht', kind="line")
        elif rete_stradale == constants.bruxells:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Bruxelles', kind="line")
        elif rete_stradale == constants.belgium:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Belgium', kind="line")
        plt.show()
    else:
        print("No item to plot")

    records, summary, keys = graph_detections.get_average_speed_filtered_by_timestamp_specific_street(min_timestamp,
                                                                                                      max_timestamp,
                                                                                                      city)
    list_of_records = []
    for record in records:
        list_of_records.append(record.data())

    if len(list_of_records) != 0:
        data_frame = pd.DataFrame.from_records(list_of_records).set_index(["timestamp"])

        if rete_stradale == constants.anderlecht:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Anderlecht', kind="line")
        elif rete_stradale == constants.bruxells:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Bruxelles', kind="line")
        elif rete_stradale == constants.belgium:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Belgium', kind="line")
        plt.show()
    else:
        print("No item to plot")


# Filtra le rilevazioni di una strada per velocita' media e veicoli
def filter_specific_street_by_vehicles_and_avg_speed(mongodb_driver, graph_detections, rete_stradale, risoluzione_temporale, periodo_tempo):

    id_street = int(input("Inserisci l'id della strada"))
    min_vehicles = int(input("Inserisci il numero minimo di veicoli su una strada"))
    max_vehicles = int(input("Inserisci il numero massimo di veicoli su una strada"))
    items = mongodb_driver.get_detections_by_id_street(id_street, rete_stradale, risoluzione_temporale, periodo_tempo)
    graph_detections.remove_old_graph()

    if rete_stradale == constants.anderlecht:
        graph_detections.execute_graph_creation(items, "Anderlecht")
        city = "Anderlecht"
    elif rete_stradale == constants.bruxells:
        graph_detections.execute_graph_creation(items, "Bruxelles")
        city = "Bruxelles"
    elif rete_stradale == constants.belgium:
        graph_detections.execute_graph_creation(items, "Belgium")
        city = "Belgium"

    records, summary, keys = graph_detections.get_timestamps_filtered_by_min_and_max_vehicles(min_vehicles,
                                                                                              max_vehicles,
                                                                                              city)

    list_of_records = []
    for record in records:
        list_of_records.append(record.data())

    if len(list_of_records) != 0:
        data_frame = pd.DataFrame.from_records(list_of_records).set_index(["timestamp"])

        if rete_stradale == constants.anderlecht:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Anderlecht', kind="line")
        elif rete_stradale == constants.bruxells:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Bruxelles', kind="line")
        elif rete_stradale == constants.belgium:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Belgium', kind="line")
        plt.show()
    else:
        print("No item to plot")

    min_avg_speed = int(input("Inserisci la minima velocita' media"))
    max_avg_speed = int(input("Inserisci la massima velocita' media"))
    records, summary, keys = graph_detections.get_timestamps_filtered_by_min_and_max_avg_speed(min_avg_speed,
                                                                                               max_avg_speed,
                                                                                               city)
    list_of_records = []
    for record in records:
        list_of_records.append(record.data())

    if len(list_of_records) != 0:
        data_frame = pd.DataFrame.from_records(list_of_records).set_index(["timestamp"])

        if rete_stradale == constants.anderlecht:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Anderlecht', kind="line")
        elif rete_stradale == constants.bruxells:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Bruxelles', kind="line")
        elif rete_stradale == constants.belgium:
            data_frame.plot(figsize=(20, 5), color='red', rot=45, title='Belgium', kind="line")
        plt.show()
    else:
        print("No item to plot")
