from neo4j import GraphDatabase
import queries

class Graph:
    def __init__(self, uri, user, password):
        self.__driver = GraphDatabase.driver(uri, auth=(user, password))

    def remove_old_graph(self):
        self.__driver.execute_query(queries.delete_graph_query)

    def execute_graph_creation(self, mongodb_cursor, city_name):
        list_od_records = []
        self.remove_old_graph()
        for item in mongodb_cursor:
            if len(list_od_records) == 10000:
                self.__driver.execute_query(queries.create_graph_query, dataset=list_od_records, city_name=city_name)
                list_od_records.clear()
            else:
                list_od_records.append(item)
        self.__driver.execute_query(queries.create_graph_query, dataset=list_od_records, city_name=city_name)
        list_od_records.clear()

    def filter_by_min_vehicles(self, min):
        records, summary, keys = self.__driver.execute_query(queries.filter_records_by_min_vehicles, min_vehicles=min)
        return records, summary, keys
    
    def filter_by_max_vehicles(self, max):
        records, summary, keys = self.__driver.execute_query(queries.filter_records_by_max_vehicles, max_vehicles=max)
        return records, summary, keys
    
    def filter_by_min_and_max_vehicles(self, min, max):
        records, summary, keys = self.__driver.execute_query(queries.filter_records_by_max_vehicles, max_vehicles=max, min_vehicles=min)
        return records, summary, keys
    
    def filter_by_min_average_speed(self, min):
        records, summary, keys = self.__driver.execute_query(queries.filter_records_by_min_average_speed, min_average_speed=min)
        return records, summary, keys
    
    def filter_by_max_average_speed(self, max):
        records, summary, keys = self.__driver.execute_query(queries.filter_records_by_max_average_speed, max_average_speed=max)
        return records, summary, keys
    
    def filter_by_min_and_max_average_speed(self, min, max):
        records, summary, keys = self.__driver.execute_query(queries.filter_records_by_min_and_max_average_speed, min_average_speed=min, max_average_speed=max)
        return records, summary, keys

    def close(self):
        self.__driver.close()

