# inspired by https://github.com/remusao/remusao.github.io

import sqlite3
import os
from random import random
import time


MAX_RECORDS = 1000000
WRITES = [str(i) for i in range(MAX_RECORDS)]
RANDOM_READS = [
    str(int(random() * MAX_RECORDS))
    for _ in range(MAX_RECORDS)
]

def bench_sqlite():
    with sqlite3.connect('db.sql') as con:
        with con:
            con.execute('CREATE TABLE store(key TEXT, value TEXT)')
        start = time.time()
        with con:
            con.executemany('INSERT INTO store VALUES (?,?)', (
                (k, 'x') for k in WRITES
            ))
        endWrite = time.time()
        with con:
            con.execute('SELECT * FROM store WHERE key in ({0})'.format(', '.join('?' for _ in RANDOM_READS)), RANDOM_READS).fetchall()
        end = time.time()
        print(f'''
        Performance for {MAX_RECORDS} items: 
        Write time - {endWrite - start} seconds
        Random read time - {end - endWrite} seconds
        ''')


if __name__ == "__main__":
    bench_sqlite()

