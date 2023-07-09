from pymongo import MongoClient

class Detections:
    def __init__(self, uri):
        self.__client = MongoClient(uri)
        self.__db = self.__client.locations

    def get_all_detections(self, city, granularity, range):
        collections = self.__db.get_collection("{city}_{granularity}_{range}".format(city=city, granularity=granularity, range=range))
        return collections.find({})

    def get_detections_by_id_street(self, id_street, city, granularity, range):
        collections = self.__db.get_collection("{city}_{granularity}_{range}".format(city=city, granularity=granularity, range=range))
        return collections.find({ "id_street": id_street })
    
    def get_detections_by_timestamp(self, timestamp, city, granularity, range):
        collections = self.__db.get_collection("{city}_{granularity}_{range}".format(city=city, granularity=granularity, range=range))
        return collections.find({ "timestamp": timestamp })
    
    def close(self):
        self.__client.close()