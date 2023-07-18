from pymongo import MongoClient
from pymongo import IndexModel
import threading

def create_indexes_thread(collection, collection_name):
    print("Creating index for: ", collection_name)
    collection.create_index("timestamp")
    collection.create_index("id_street")
    print("Index created for: ", collection_name)

string_connection = input("Inserire la stringa di connessione di mongoDB: ")
client = MongoClient(string_connection)
db = client["detections"]

threads = []

for collection_name in db.list_collection_names():
    collection = db.get_collection(collection_name)
    threads.append(threading.Thread(target=create_indexes_thread, args=(collection, collection_name)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

