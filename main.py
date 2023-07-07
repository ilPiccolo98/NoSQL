from pymongo import MongoClient
from neo4j import GraphDatabase

client = MongoClient("mongodb://localhost:27017")
db = client.locations
collections = db.get_collection("And_05min_0101_0103_2019")
items = collections.find({}).limit(5)

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "nosqlproject"))

for item in items:
    driver.execute_query("CREATE (n:LOCATION {timestamp: $timestamp, id_street: $id_street, vehicles: $vehicles, average_speed: $average_speed})", 
                         timestamp=item["timestamp"], id_street=item["id_street"], vehicles=item["vehicles"], average_speed=item["average_speed"])
result = driver.execute_query("MATCH (n:LOCATION) RETURN n")
for record in result.records:
    print(record.data())

client.close()
driver.close()
