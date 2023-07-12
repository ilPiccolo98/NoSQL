delete_graph_query = "MATCH (n) DETACH DELETE n"

create_graph_query = '''  MERGE (city:CITY {name: $city_name})
                          WITH $dataset AS batch 
                          UNWIND batch AS node 
                          MERGE (street:STREET {id_street: node.id_street})
                          MERGE (street) -[r_street:IS_IN]-> (city)
                          CREATE (detection:DETECTION {timestamp: node.timestamp})
                          CREATE (detection) -[r_detection:DETECTED_AT {vehicles: node.vehicles, average_speed: node.average_speed}]-> (street)
                        '''

filter_records_by_min_vehicles = '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
                                    WHERE r.vehicles >= $min_vehicles
                                    return detection.timestamp, r.vehicles, r.average_speed, street.id_street
                                    ''' 

filter_records_by_max_vehicles = '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
                                    WHERE r.vehicles <= $max_vehicles
                                    return detection.timestamp, r.vehicles, r.average_speed, street.id_street
                                    ''' 


filter_records_by_min_and_max_vehicles = '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
                                            WHERE r.vehicles >= $min_vehicles and r.vehicles <= $max_vehicles
                                            return detection.timestamp, r.vehicles, r.average_speed, street.id_street
                                            '''

filter_records_by_min_average_speed = '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
                                        WHERE r.average_speed >= $min_average_speed
                                        return detection.timestamp, r.vehicles, r.average_speed, street.id_street
                                        '''

filter_records_by_max_average_speed = '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
                                        WHERE r.average_speed <= $max_average_speed
                                        return detection.timestamp, r.vehicles, r.average_speed, street.id_street
                                        '''


filter_records_by_min_and_max_average_speed = '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
                                                 WHERE r.average_speed >= $min_average_speed and r.average_speed <= $max_average_speed
                                                 return detection.timestamp, r.vehicles, r.average_speed, street.id_street
                                              '''