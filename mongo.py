from pymongo import MongoClient


def get_collection(mongo_user, mongo_password, collection_name):
    client = MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@vectorpoccluster.x92pk.mongodb.net/?retryWrites=true&w=majority&appName=VectorPocCluster")
    db = client['ragpoc']
    return db[collection_name]
