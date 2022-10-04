import yottadb
import time
from random import random

# random reads and writes
MAX_RECORDS = 10000
WRITES = [str(i) for i in range(MAX_RECORDS)]
RANDOM_READS = [
    str(int(random() * MAX_RECORDS))
    for _ in range(MAX_RECORDS)
]

# creating a wrapper for yottadb

class YottaWraper:
    def __init__(self, glo):
        self.glo = glo
    
    def __setitem__(self, key, value):
        yottadb.set(self.glo, [key], value)
    
    def __getitem__(self, key):
        return yottadb.get(self.glo, [key])

# create yottadb wrapper cursor
cur = YottaWraper("^test")

# -- WRITE TEST --
# start timer
start = time.time()

for i in WRITES:
    cur[i] = "x"
endWrite = time.time()

for i in RANDOM_READS:
    x = cur[i]

end = time.time()
print(f'''
Performance for {MAX_RECORDS} items: 
Write time - {endWrite - start} seconds
Random read time - {end - endWrite} seconds
''')

# -- BULK WRITE TEST --

# YottaDB
'''
@yottadb.transaction
def test_transaction(key0: yottadb.Key) -> None:
    data = ""
    for i in range(500000):
        data=f"{i}"
        key0[data].value = data

key0 = yottadb.Key("^test")
status = test_transaction(key0)

if status != yottadb.YDB_OK:
    # Well... fuck
    print("ABORT, MISSION FAILED")
else:
    end = time.time()
    print(f'writing 500k items to a global: {end - start} seconds')
'''
