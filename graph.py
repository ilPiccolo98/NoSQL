from neo4j import GraphDatabase
import queries

class Graph:
    def __init__(self, uri, user, password):
        self.__driver = GraphDatabase.driver(uri, auth=(user, password))

    def remove_old_graph(self):
        self.__driver.execute_query(queries.delete_graph_query)

    def execute_graph_creation(self, mongodb_cursor, city_name):
        self.__driver.execute_query(queries.create_city_node, city_name=city_name)
        list_of_records = []
        for item in mongodb_cursor:
            if len(list_of_records) == 10000:
                self.__driver.execute_query(queries.create_graph_query, dataset=list_of_records, city_name=city_name)
                list_of_records.clear()
            else:
                list_of_records.append(item)
        self.__driver.execute_query(queries.create_graph_query, dataset=list_of_records, city_name=city_name)
        list_of_records.clear()

    def filter_records_by_vehicles_and_speed(self, min_vehicles, max_vehicles, min_average_speed, max_average_speed, city_name):
        records, summary, keys = self.__driver.execute_query(queries.filter_records_by_vehicles_and_speed, min_vehicles=min_vehicles, 
                                                             max_vehicles=max_vehicles, min_average_speed=min_average_speed, 
                                                             max_average_speed=max_average_speed, city_name=city_name)
        return records, summary, keys

    def get_vehicles_filtered_by_timestamp_specific_street(self, min_timestamp, max_timestamp, city_name):
        records, summary, keys = self.__driver.execute_query(queries.vehicles_filtered_by_timestamp_specific_street, 
                                                             min_timestamp=min_timestamp, max_timestamp=max_timestamp, city_name=city_name)
        return records, summary, keys
    
    def get_average_speed_filtered_by_timestamp_specific_street(self, min_timestamp, max_timestamp, city_name):
        records, summary, keys = self.__driver.execute_query(queries.average_speed_filtered_by_timestamp_specific_street, 
                                                             min_timestamp=min_timestamp, max_timestamp=max_timestamp, city_name=city_name)
        return records, summary, keys

    def get_timestamps_filtered_by_min_and_max_vehicles(self, min_vehicles, max_vehicles, city_name):
        records, summary, keys = self.__driver.execute_query(queries.timestamps_filtered_by_min_and_max_vehicles, 
                                                             min_vehicles=min_vehicles, max_vehicles=max_vehicles, city_name=city_name)
        return records, summary, keys

    def get_timestamps_filtered_by_min_and_max_avg_speed(self, min_average_speed, max_average_speed, city_name):
        records, summary, keys = self.__driver.execute_query(queries.timestamps_filtered_by_min_and_max_avg_speed, 
                                                             min_average_speed=min_average_speed, max_average_speed=max_average_speed, city_name=city_name)
        return records, summary, keys

    def close(self):
        self.__driver.close()

