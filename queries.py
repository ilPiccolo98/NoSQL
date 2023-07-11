delete_graph_query = "MATCH (n) DETACH DELETE n"

def create_city_node_query(city_name):
    return "CREATE (n:CITY {name: '%s'})" % city_name

def create_graph(id_street, timestamp, vehicles, average_speed, city_name):
    return '''MATCH (city:CITY) WHERE city.name = '%s' 
              MERGE (street:STREET {id_street: %f})
              MERGE (street) -[r_street:IS_IN]-> (city)
              CREATE (detection:DETECTION {timestamp: '%s'})
              CREATE (detection) -[r_detection:DETECTED_AT {vehicles: %d, average_speed: %f}]-> (street)
              ''' % (city_name, id_street, timestamp, vehicles, average_speed)

def get_records_filtered_by_min_vehicles(min):
    return '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
              WHERE r.vehicles >= %d
              return detection.timestamp, r.vehicles, r.average_speed, street.id_street
            ''' % min

def get_records_filtered_by_max_vehicles(max):
    return '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
              WHERE r.vehicles <= %d
              return detection.timestamp, r.vehicles, r.average_speed, street.id_street
            ''' % max

def get_records_filtered_by_min_and_max_vehicles(min, max):
    return '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
              WHERE r.vehicles >= %d and r.vehicles <= %d
              return detection.timestamp, r.vehicles, r.average_speed, street.id_street
            ''' % (min, max)

def get_records_filtered_by_min_average_speed(min):
    return '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
              WHERE r.average_speed >= %d
              return detection.timestamp, r.vehicles, r.average_speed, street.id_street
            ''' % min

def get_records_filtered_by_max_average_speed(max):
    return '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
              WHERE r.average_speed <= %d
              return detection.timestamp, r.vehicles, r.average_speed, street.id_street
            ''' % max

def get_records_filtered_by_min_and_max_average_speed(min, max):
    return '''MATCH (detection:DETECTION) -[r:DETECTED_AT]-> (street:STREET)
              WHERE r.average_speed >= %d and r.average_speed <= %d
              return detection.timestamp, r.vehicles, r.average_speed, street.id_street
            ''' % (min, max)