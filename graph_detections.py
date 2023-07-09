from graph import Graph
import queries


class Graph_detections:
    def __init__(self, uri, user, password):
        self.__graph = Graph(uri, user, password)
    
    def create_graph(self, dataset, city_name):
        self.__graph.execute_query(queries.delete_graph_query)
        self.__graph.execute_query(queries.create_city_node_query(city_name))
        print("Before __get_streets")
        print("dataset:", len(list(dataset)))
        street_ids = self.__get_streets(dataset)
        print("After __get_streets")
        print("dataset:", len(list(dataset)))
        self.__add_streets_into_graph(street_ids, city_name)
        self.__add_detections_into_graph(dataset)
        
    def close(self):
        self.__graph.close()

    def __add_streets_into_graph(self, street_ids, city_name):
        for street_id in street_ids:
            self.__graph.execute_query(queries.create_street_node_query(street_id, city_name))

    def __add_detections_into_graph(self, items):
        print("Inside __add_detections_into_graph")
        print("Items:", len(list(items)))
        for item in items:
            self.__graph.execute_query(queries.create_detection_node_query(item["timestamp"], item["vehicles"], item["average_speed"], item["id_street"]))

    def __get_streets(self, dataset):
        street_ids = set()
        for item in dataset:
            street_ids.add(item["id_street"])
        return street_ids