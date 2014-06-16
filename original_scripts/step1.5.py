# This creates the result matrices for plate crossings

import psycopg2
import json
from config import *

# Connect to the database
try:
  conn = psycopg2.connect(dbname="alice", user=user_name, host=host_name, port=port_no)
except:
  print "Unable to connect"

cur = conn.cursor()


### This creates the result matrices

# Create the matrices to hold the results
plates_year_matrix_query250 = "CREATE TABLE gaps250 ( year integer PRIMARY KEY, "
plates_year_matrix_query500 = "CREATE TABLE gaps500 ( year integer PRIMARY KEY, "
plates_year_matrix_query1000 = "CREATE TABLE gaps1000 ( year integer PRIMARY KEY, "
plates_year_matrix_query1500 = "CREATE TABLE gaps1500 ( year integer PRIMARY KEY, "

middle = ""
# Add everything north of the equator
x = 89
while x > 0:
  toAdd =  "n" + str(x) + " numeric, "
  middle += toAdd
  x -= 1

# Add the equator
middle += "x0 numeric, "

# Add everything south of the equator
x = 1
while x < 90:
  toAdd =  "s" + str(x) + " numeric, "
  middle += toAdd
  x += 1

# Clean up the slop
middle = middle.rstrip(', ')
middle += ")"


cur.execute(plates_year_matrix_query250 + middle);
conn.commit();

cur.execute(plates_year_matrix_query500 + middle);
conn.commit();

cur.execute(plates_year_matrix_query1000 + middle);
conn.commit();

cur.execute(plates_year_matrix_query1500 + middle);
conn.commit();

# Insert a placeholder for each year row
i = 0
while i < 551:
  cur.execute("INSERT INTO gaps250 (year) VALUES (" + str(i) + ")")
  conn.commit()
  cur.execute("INSERT INTO gaps500 (year) VALUES (" + str(i) + ")")
  conn.commit()
  cur.execute("INSERT INTO gaps1000 (year) VALUES (" + str(i) + ")")
  conn.commit()
  cur.execute("INSERT INTO gaps1500 (year) VALUES (" + str(i) + ")")
  conn.commit()
  i += 1

print "Done!"