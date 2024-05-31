from pymongo import MongoClient, errors
import config


class Database:
    def __init__(self):
        try:
            self.connection = MongoClient(config.DB_CONNECTION_URI)
            self.db = self.connection[config.DB_NAME]
            self.order_collection = self.db[config.DB_COL_ORDER]
            self.harga_collection = self.db[config.DB_COL_HARGA]
        except errors.ConnectionFailure as con_err:
            print(f"Koneksi gagal (Connection Failure)| {con_err}")
        except Exception as err:
            print(f"Koneksi gagal (Others)| {err}")
