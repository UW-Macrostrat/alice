import multiprocessing
import argparse
from lym_lat import *
import numpy as np
import psycopg2
from psycopg2.extensions import AsIs
from credentials import *

connection = psycopg2.connect(dbname="alice", user=pg_user, host=pg_host, port=pg_port)
cursor = connection.cursor()

sql = "DROP TABLE IF EXISTS plate_length_year_can_lat; CREATE TABLE plate_length_year_can_lat ( year integer, plateid integer, coord numeric, the_length numeric)"
'''
sql_lats = []

for lat in np.arange(-89.5, 89.5, 0.5):
    if lat < 0:
        sql_lats.append("s" + "{0:g}".format(float(abs(lat))))
    elif lat > 0:
        sql_lats.append("n" + "{0:g}".format(float(abs(lat))))
    else:
        sql_lats.append("x" + "{0:g}".format(float(abs(lat))))

sql += ", ".join(sql_lats) + ")"
'''
cursor.execute(sql)
connection.commit()

tasks = multiprocessing.JoinableQueue()
results = multiprocessing.Queue()

num_processors = multiprocessing.cpu_count() - 1
processors = [Processor(tasks, results) for i in xrange(num_processors)]

for each in processors:
    each.start()

for i in xrange(551):
    tasks.put(Task(i))

for i in range(num_processors):
    tasks.put(None)
