import pymongo
from random import random
import time

MAX_RECORDS = 1000000
WRITES = [str(i) for i in range(MAX_RECORDS)]
RANDOM_READS = [
    str(int(random() * MAX_RECORDS))
    for _ in range(MAX_RECORDS)
]

client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database("test")
db = client["test"]
col = db["values"]

# clear database


customers_list = []
for i in WRITES:
    temp = {"_id": i}
    temp[i] = "x"
    customers_list.append(temp)

start = time.time()
x = col.insert_many(customers_list)
endWrite = time.time()
end = 0

print(f"writing {MAX_RECORDS} - {endWrite - start} seconds")

for i in RANDOM_READS:
    x = col.find_one({"_id": i})
end = time.time()

print(f'''
Performance for {MAX_RECORDS} items: 
Write time - {endWrite - start} seconds
Random read time - {end - endWrite} seconds
''')

# print list of the _id values of the inserted documents:
# print(x.inserted_ids)
