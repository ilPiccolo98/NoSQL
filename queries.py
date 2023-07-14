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

filter_records_by_vehicles_and_speed = '''MATCH (city:CITY)
                                          WHERE city.name = $city_name
                                          MATCH (city:CITY) -[r_has:HAS]-> (street:STREET)
                                          MATCH (street:STREET) -[r_detected:DETECTED]-> (detection:DETECTION)
                                          WHERE detection.vehicles >= $min_vehicles and detection.vehicles <= $max_vehicles and
                                                detection.average_speed >= $min_average_speed and detection.average_speed <= $max_average_speed
                                          return r_detected.timestamp as timestamp, detection.vehicles as vehicles, detection.average_speed as average_speed, street.id_street as id_street
                                        '''

vehicles_filtered_by_timestamp_specific_street = '''MATCH (city:CITY)
                                                    WHERE city.name = $city_name
                                                    MATCH (city) -[r_has:HAS]-> (street:STREET)
                                                    MATCH (street) -[r_detected:DETECTED]-> (detection:DETECTION)
                                                    WHERE r_detected.timestamp >= $min_timestamp and 
                                                    r_detected.timestamp <= $max_timestamp
                                                    return r_detected.timestamp as timestamp, detection.vehicles as vehicles
                                                    order by r_detected.timestamp
                                                    '''

average_speed_filtered_by_timestamp_specific_street = '''MATCH (city:CITY)
                                                         WHERE city.name = $city_name
                                                         MATCH (city) -[r_has:HAS]-> (street:STREET)
                                                         MATCH (street) -[r_detected:DETECTED]-> (detection:DETECTION)
                                                         WHERE r_detected.timestamp >= $min_timestamp and 
                                                         r_detected.timestamp <= $max_timestamp
                                                         return r_detected.timestamp as timestamp, detection.average_speed as average_speed
                                                         order by r_detected.timestamp
                                                        '''
