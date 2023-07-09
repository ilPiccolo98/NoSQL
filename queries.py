delete_graph_query = "MATCH (n) DETACH DELETE n"

def create_city_node_query(city_name):
    return "CREATE (n:CITY {name: '%s'})" % city_name

def create_street_node_query(street_id, city_name):
    return '''MATCH (city:CITY) WHERE city.name = '%s' 
              CREATE (street:STREET {id_street: %f})
              CREATE (street) -[r:IS_IN]-> (city)''' % (city_name, street_id)

def create_detection_node_query(timestamp, vehicles, average_speed, id_street):
    return '''MATCH (street:STREET) where street.id_street = %f
              CREATE (detection:DETECTION {timestamp: '%s'})
              CREATE (detection) -[r:DETECTED_AT {vehicles: %d, average_speed: %f}]-> (street)
            ''' % (id_street, timestamp, vehicles, average_speed)