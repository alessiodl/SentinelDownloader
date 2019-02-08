from sentinelsat import SentinelAPI
import os

username = 'mySciHubUsername'
password = 'mySciHubPassword'
api = SentinelAPI(username, password)

download_dir = r"C:\Users\username\Desktop\download"

# Lista di product id (sostituire con quelli reali)
products = [
    '22167cb1-19e4-4998-a191-b48084cdcc6d',
    '555384f1-a447-4fbb-a8fb-f7da39c270f9',
    'f909147f-b935-49fb-83bc-469980694152'
]

api.download_all(products, download_dir)
