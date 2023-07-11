from graph import Graph
import queries


class Graph_detections:
    def __init__(self, uri, user, password):
        self.__graph = Graph(uri, user, password)
    
    def create_graph(self, dataset, city_name):
        self.__graph.execute_query(queries.delete_graph_query)
        self.__graph.execute_query(queries.create_city_node_query(city_name))
        for item in dataset:
            if "timestamp" in item:
                self.__graph.execute_query(queries.create_graph(item["id_street"], item["timestamp"], 
                                                                item["vehicles"], item["average_speed"], city_name))

    def filter_by_min_vehicles(self, min):
        records, summary, keys = self.__graph.execute_query(queries.get_records_filtered_by_min_vehicles(min))
        return records, summary, keys
    
    def filter_by_max_vehicles(self, max):
        records, summary, keys = self.__graph.execute_query(queries.get_records_filtered_by_max_vehicles(max))
        return records, summary, keys
    
    def filter_by_min_and_max_vehicles(self, min, max):
        records, summary, keys = self.__graph.execute_query(queries.get_records_filtered_by_min_and_max_vehicles(min, max))
        return records, summary, keys
    
    def filter_by_min_average_speed(self, min):
        records, summary, keys = self.__graph.execute_query(queries.get_records_filtered_by_min_average_speed(min))
        return records, summary, keys
    
    def filter_by_max_average_speed(self, max):
        records, summary, keys = self.__graph.execute_query(queries.get_records_filtered_by_max_average_speed(max))
        return records, summary, keys
    
    def filter_by_min_and_max_average_speed(self, min, max):
        records, summary, keys = self.__graph.execute_query(queries.get_records_filtered_by_min_and_max_average_speed(min, max))
        return records, summary, keys
        
    def close(self):
        self.__graph.close()