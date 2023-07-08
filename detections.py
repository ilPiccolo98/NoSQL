from pymongo import MongoClient

class Detections:
    def __init__(self, uri):
        self.__client = MongoClient(uri)
        self.__db = self.__client.locations

    def get_data(self, city, granularity, range):
        collections = self.__db.get_collection("{city}_{granularity}_{range}".format(city=city, granularity=granularity, range=range))
        return collections.find({})
    
    def close(self):
        self.__client.close()