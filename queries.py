delete_graph_query = "MATCH (n) DETACH DELETE n"

create_city_node = '''CREATE (city:CITY {name: $city_name})'''

create_graph_query = '''  WITH $dataset AS batch 
                          UNWIND batch AS node 
                          MATCH (city:CITY)
                          WHERE city.name = $city_name
                          MERGE (street:STREET {id_street: node.id_street})
                          MERGE (city) -[r_city:HAS]-> (street)
                          CREATE (detection:DETECTION {vehicles: node.vehicles, average_speed: node.average_speed})
                          CREATE (street) -[r_street:DETECTED {timestamp: node.timestamp}]-> (detection)
                        '''

filter_records_by_min_vehicles = '''MATCH (city:CITY)
                                    WHERE city.name = $city_name
                                    MATCH (street:STREET) -[r:DETECTED]-> (detection:DETECTION)
                                    WHERE detection.vehicles >= $min_vehicles
                                    return r.timestamp, detection.vehicles, detection.average_speed, street.id_street
                                    ''' 

filter_records_by_max_vehicles = '''MATCH (city:CITY)
                                    WHERE city.name = $city_name
                                    MATCH (street:STREET) -[r:DETECTED]-> (detection:DETECTION)
                                    WHERE detection.vehicles <= $max_vehicles
                                    return r.timestamp, detection.vehicles, detection.average_speed, street.id_street
                                    ''' 


filter_records_by_min_and_max_vehicles = '''MATCH (city:CITY)
                                            WHERE city.name = $city_name
                                            MATCH (street:STREET) -[r:DETECTED]-> (detection:DETECTION)
                                            WHERE detection.vehicles <= $max_vehicles and r.vehicles >= $min_vehicles
                                            return r.timestamp, detection.vehicles, detection.average_speed, street.id_street
                                            '''

filter_records_by_min_average_speed = '''MATCH (city:CITY)
                                         WHERE city.name = $city_name
                                         MATCH (street:STREET) -[r:DETECTED]-> (detection:DETECTION)
                                         WHERE detection.average_speed >= $min_average_speed
                                         return r.timestamp, detection.vehicles, detection.average_speed, street.id_street
                                        '''

filter_records_by_max_average_speed = '''MATCH (city:CITY)
                                         WHERE city.name = $city_name
                                         MATCH (street:STREET) -[r:DETECTED]-> (detection:DETECTION)
                                         WHERE detection.average_speed <= $max_average_speed
                                         return r.timestamp, detection.vehicles, detection.average_speed, street.id_street
                                        '''


filter_records_by_min_and_max_average_speed = '''MATCH (city:CITY)
                                                 WHERE city.name = $city_name
                                                 MATCH (street:STREET) -[r:DETECTED]-> (detection:DETECTION)
                                                 WHERE detection.average_speed >= $min_average_speed and detection.average_speed <= $max_average_speed
                                                 return r.timestamp, detection.vehicles, detection.average_speed, street.id_street
                                                '''