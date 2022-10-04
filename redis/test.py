import redis
import time
from random import random

# r = redis.Redis(host='localhost', port=6379,password=0)

class RedisWraper:
    def __init__(self, host, port, password):
        self.cur = redis.Redis(host, port, password)
    
    def __setitem__(self, key, value):
        self.cur.set(key, value)

    def __getitem__(self, key):
        return self.cur.get(key)

MAX_RECORDS = 1000000
WRITES = [str(i) for i in range(MAX_RECORDS)]
RANDOM_READS = [
    str(int(random() * MAX_RECORDS))
    for _ in range(MAX_RECORDS)
]

'''
With pipelining
'''
def attempt2(cursor):
    pipe = cursor.cur.pipeline()
    start = time.time()

    for i in WRITES:
        data=f"{i}"
        pipe.set(data, data)

    pipe.execute()
    endWrite = time.time()
    for i in RANDOM_READS:
        x = cursor[i]
    end = time.time()

    print(f'''
        Performance for {MAX_RECORDS} items: 
        Write time - {endWrite - start} seconds
        Random read time - {end - endWrite} seconds
        ''')

'''
Without pipelining
'''
def attempt1(cursor):
    start = time.time()
    for i in WRITES:
        cursor[i] = "x"
    endWrite = time.time()
    for i in RANDOM_READS:
        x = cursor[i]
    end = time.time()
    print(f'''
        Performance for {MAX_RECORDS} items: 
        Write time - {endWrite - start} seconds
        Random read time - {end - endWrite} seconds
        ''')

r = RedisWraper("localhost", 6379,0)
# attempt1(r)
attempt2(r)


'''
With pipelining
'''

''' 
# attempt 1

start = time.time()
data = ""

for i in range(500000):
    data=f"{i}"
    r.set(data, data)

end = time.time()
print(f'writing 500k items in redis: {end - start} seconds')
'''

'''
pipe = r.pipeline()
start = time.time()

for i in range(500000):
    data=f"{i}"
    pipe.set(data, data)

pipe.execute()
end = time.time()
print(f'writing 500k items in redis: {end - start} seconds')
'''
