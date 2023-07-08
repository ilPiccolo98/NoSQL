from neo4j import GraphDatabase


class Graph:
    def __init__(self, uri, user, password):
        self.__driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def execute_query(self, query):
        self.__driver.execute_query(query)

    def close(self):
        self.__driver.close()

