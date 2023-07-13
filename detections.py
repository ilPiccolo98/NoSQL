from pymongo import MongoClient
import gridfs
import json

class Detections:
    def __init__(self, uri):
        self.__client = MongoClient(uri)
        self.__db = self.__client.detections
        self.__gridfs = gridfs.GridFS(self.__client.gridfs)

    def get_Anderlecht_streets(self):
        data = self.__gridfs.find({ "filename": "Anderlecht_streets.json" }).next().read()
        return json.loads(data)
    
    def get_Bruxelles_streets(self):
        data = self.__gridfs.find({ "filename": "Bruxelles_streets.json" }).next().read()
        return json.loads(data)

    def get_Belgium_streets(self):
        data = self.__gridfs.find({ "filename": "Belgium_streets.json" }).next().read()
        return json.loads(data)

    def get_all_detections(self, city, granularity, range):
        collections = self.__db.get_collection("{city}_{granularity}_{range}".format(city=city, granularity=granularity, range=range))
        return collections.find({}, {'_id': False})
    
    def get_all_detections_group_by_timestamp_sum_vehicles(self, city, granularity, range):
        collections = self.__db.get_collection("{city}_{granularity}_{range}".format(city=city, granularity=granularity, range=range))
        return collections.aggregate([ { "$match": { "timestamp": { "$exists": "true", "$ne": "null"} } }, { "$group": { "_id": "$timestamp", "vehicles": { "$sum": "$vehicles" } } }, { "$sort": { "_id": 1 } } ])

    def get_all_detections_group_by_timestamp_avg_vehicles(self, city, granularity, range):
        collections = self.__db.get_collection("{city}_{granularity}_{range}".format(city=city, granularity=granularity, range=range))
        return collections.aggregate([ { "$match": { "timestamp": { "$exists": "true", "$ne": "null"} } }, { "$group": { "_id": "$timestamp", "vehicles": { "$avg": "$vehicles" } } }, { "$sort": { "_id": 1 } } ])

    def get_detections_by_id_street(self, id_street, city, granularity, range):
        collections = self.__db.get_collection("{city}_{granularity}_{range}".format(city=city, granularity=granularity, range=range))
        return collections.find({ "id_street": id_street }, {'_id': False})
    
    def get_detections_by_timestamp(self, timestamp, city, granularity, range):
        collections = self.__db.get_collection("{city}_{granularity}_{range}".format(city=city, granularity=granularity, range=range))
        return collections.find({ "timestamp": timestamp }, {'_id': False})
    
    def get_number_of_streets_anderlecht(self):
        data = self.__gridfs.find({ "filename": "Anderlecht_streets.json" }).next().read()
        geoJson = json.loads(data)
        return len(geoJson["features"])

    def get_number_of_streets_bruxelles(self):
        data = self.__gridfs.find({ "filename": "Bruxelles_streets.json" }).next().read()
        geoJson = json.loads(data)
        return len(geoJson["features"])
    
    def get_number_of_streets_belgium(self):
        data = self.__gridfs.find({ "filename": "Belgium_streets.json" }).next().read()
        geoJson = json.loads(data)
        return len(geoJson["features"])

    def close(self):
        self.__client.close()