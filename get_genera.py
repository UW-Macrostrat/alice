'''
CREATE EXTENSION intarray;

CREATE TABLE plate_genera (
  id SERIAL PRIMARY KEY,
  plateid       int,
  year          int,
  genera        text[],
  genera_count  int
)
'''
import os
import sys
import psycopg2
import MySQLdb
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

def get_genera(year):
  cur.execute("""
    SELECT DISTINCT plateid FROM reconstructed_""" + str(year) + """_merged
  """)

  # Get all plates for the given year
  distinct_plates = cur.fetchall()

  # For each plate, find the number of genera, given the current year
  for plate in distinct_plates:
    mysql_cur.execute("""

      SELECT distinct genus_name c 
      FROM occ_matrix 
        JOIN paleocoords USING (collection_no) 
      WHERE plate_no= """ + str(plate[0]) + """ 
        AND paleocoords.early_age>= """ + str(year) + """ 
        AND paleocoords.late_age<= """ + str(year) + """

    """)

    plate_genera = mysql_cur.fetchall()

    #genera_string = "{"
    genera = []

    for genus in plate_genera:
      genera.append(genus[0])
      #genera_string += genus[0] + ", "

    #if len(genera_string) > 1:
    #  genera_string = genera_string[:-2]
    #genera_string += "}"

    #print genera_string

    cur.execute("INSERT INTO plate_genera (plateid, year, genera) VALUES( %s, %s, %s)", (plate[0], year, genera))

    conn.commit()


for year in xrange(0, 551):
  get_genera(year)
  print "----- Done with year " + str(year) + " ------"