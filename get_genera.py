'''
Make sure this is run first

CREATE TABLE plate_genera (
  id SERIAL PRIMARY KEY,
  plateid       int,
  year          int,
  genera        int[],
  genera_count  int
);

'''
import os
import sys
import psycopg2
import MySQLdb
import urllib2
import json
from config import *

# Connect to the database
try:
  conn = psycopg2.connect(dbname="alice", user=user_name, host=host_name, port=port_no)
except:
  print "Could not connect to database: ", sys.exc_info()[1]
  sys.exit()

# Create a cursor for executing queries
cur = conn.cursor()

try:
  mysql_conn = MySQLdb.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, unix_socket=mysql_unix_socket)
except:
  print "Could not connect to database: ", sys.exc_info()[1]
  sys.exit()

# Cursor for MySQL
mysql_cur = mysql_conn.cursor()
print mysql_cur

def get_genera(year):
  print "Working on ", year

  cur.execute("""
    SELECT DISTINCT plateid FROM reconstructed_""" + str(year) + """_merged
  """)

  # Get all plates for the given year
  distinct_plates = cur.fetchall()

  # For each plate, find the number of genera, given the current year
  for plate in distinct_plates:
    mysql_cur.execute("""

      SELECT DISTINCT t.orig_no 
      FROM taxon_trees AS t 
        JOIN occ_matrix AS o USING (orig_no) 
        JOIN paleocoords AS pc USING (collection_no) 
          WHERE plate_no = %(plate)s 
          AND pc.early_age >= %(year)s
          AND pc.late_age <= %(year)s 
          AND rank = 5

    """, {
          "plate": plate[0], 
          "year" : year
         }
    )

    plate_genera = mysql_cur.fetchall()

    print "Got plate genera for plate " + str(plate[0]) + " in year " + str(year)

    # Convert the results to a single dimensional python list
    genera = []
    for genus in plate_genera:
      genera.append(genus[0])

    cur.execute("INSERT INTO plate_genera (plateid, year, genera) VALUES( %s, %s, %s)", (plate[0], year, genera))

    conn.commit()

# Get stage midpoints
midpoints = []
time_data = json.load(urllib2.urlopen('http://paleobiodb.org/data1.1/intervals/list.json?scale=1&order=older&max_ma=4000'))
for interval in time_data['records']:
  if interval['lvl'] == 5:
    midpoint = int((interval['lag'] + interval['eag'])/2)
    if midpoint not in midpoints:
      midpoints.append(midpoint)

print "Got midpoints"

# Iterate over each year
for year in xrange(0, 551):
#for year in midpoints:
  #if year not in midpoints:
  get_genera(year)
  print "----- Done with year " + str(year) + " ------"

# Finish up by filling the field `genera_count`
cur.execute("UPDATE plate_genera SET genera_count = array_length(genera, 1)")
conn.commit()
print "Done!"