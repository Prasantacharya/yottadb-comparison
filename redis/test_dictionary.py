import redis
import time
from random import random

# r = redis.Redis(host='localhost', port=6379,password=0)

class Wraper:
    def __init__(self):
        self.cur = {}
    
    def __setitem__(self, key, value):
        self.cur[key] = value

    def __getitem__(self, key):
        return self.cur[key]

MAX_RECORDS = 1000000
WRITES = [str(i) for i in range(MAX_RECORDS)]
RANDOM_READS = [
    str(int(random() * MAX_RECORDS))
    for _ in range(MAX_RECORDS)
]

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

r = Wraper()
attempt1(r)
# attempt2(r)


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
