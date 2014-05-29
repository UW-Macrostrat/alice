import sys
import psycopg2
from config import *

# Connect to the database
try:
  conn = psycopg2.connect(dbname="alice", user=user_name, host=host_name, port=port_no)
except:
  print "Could not connect to database: ", sys.exc_info()[1]
  sys.exit()

# Create a cursor for executing queries
cur = conn.cursor()

# Get all plate ids
cur.execute("SELECT plateid FROM name_lookup")
plates = cur.fetchall()

# Build the table creation / destruction query
query = "DROP TABLE IF EXISTS areas; CREATE TABLE areas (year integer, "

for plate in plates:
  query += "p" + str(plate[0]) + " numeric, "

query = query[:-2] + ")"

cur.execute(query)
conn.commit()

# Insert a row for each year into the table
for year in xrange(0, 551):
  cur.execute("INSERT INTO areas (year) VALUES (%s)", [year])

conn.commit()

# Find the area of each plate in each year and add the result to the `areas` table
for plate in plates:
  for year in xrange(0, 551):
    cur.execute("UPDATE areas SET p" + str(plate[0]) + " = (SELECT ST_Area(geom::geography)/1000 FROM reconstructed_" + str(year) + "_merged WHERE plateid = %s) WHERE year = %s", [plate[0], year])
  conn.commit()
  print "Done with plate", plate[0]

# Clean up one error
cur.execute("UPDATE areas SET p802 = (((SELECT p802 FROM areas WHERE year = 316) + (SELECT p802 FROM areas WHERE year = 318))/2) WHERE year = 317")
conn.commit()

# Update `name_lookup` with the average area of each plate
for plate in plates:
  cur.execute("UPDATE name_lookup SET area = (SELECT avg(p" + str(plate[0]) + ") FROM areas) WHERE plateid = " + str(plate[0]))

conn.commit()
