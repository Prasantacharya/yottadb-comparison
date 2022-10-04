import mysql.connector
import os
from random import random
import time


MAX_RECORDS = 1000000
WRITES = [str(i) for i in range(MAX_RECORDS)]
RANDOM_READS = [
    str(int(random() * MAX_RECORDS))
    for _ in range(MAX_RECORDS)
]

def bench():
    cnx = mysql.connector.connect(
    host="localhost",
    port=30306,
    user="root",
    password="1")

    cur = cnx.cursor()

    TABLES = {}
    TABLES['test'] = (
        "CREATE TABLE `test` ("
        "  `key` VARCHAR(5) NOT NULL,"
        "  `value` varchar(14) NOT NULL,"
        "  PRIMARY KEY (`key`)"
        ") ENGINE=InnoDB")
    cur.execute("CREATE DATABASE IF NOT EXISTS test")
    cur.execute("USE test")
    cur.execute("DROP TABLE IF EXISTS a")
    cur.execute("CREATE TABLE IF NOT EXISTS a( key1 VARCHAR(255) PRIMARY KEY, value1 VARCHAR(6) ) ENGINE=INNODB;")

    
    insert_items = []
    select_items=[]
    query = "INSERT INTO a(key1, value1) VALUES(%s, %s)"
    for rec in WRITES:
        insert_items.append((rec, "x"))
        select_items.append((rec,))
    start = time.time()
    cur.executemany(query,insert_items)
    endWrite = time.time()
    print(f'''
        Performance for {MAX_RECORDS} items:
        Write time - {endWrite - start} 
        ''')
    
    query = "SELECT value1 FROM a WHERE (key1) IN (%s)"
    cur.executemany(query,select_items)
    end = time.time()
    print(f'''
        Performance for {MAX_RECORDS} items: 
        Write time - {endWrite - start} seconds
        Random read time - {end - endWrite} seconds
        ''')


if __name__ == "__main__":
    bench()