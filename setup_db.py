# Step 0 creates the base tables, including GPlates geometry and the graticule

import os
import sys
import psycopg2
from config import *

os.system("psql -f create_alice.sql")

# Connect to the database
try:
  conn = psycopg2.connect(dbname="alice", user=user_name, host=host_name, port=port_no)
except:
  print "Could not connect to database: ", sys.exc_info()[1]
  sys.exit()

# Create a cursor for executing queries
cur = conn.cursor()

i = 0
while i < 551:
  shapefileName = "reconstructed_" + str(i) + ".00Ma.shp"
  os.system("shp2pgsql -s 4326 polygons_550_to_0Ma/Phanerozoic_EarthByte_Coastlines/" + shapefileName + " public." + shapefileName.split(".")[0] + " | psql -h " + host_name + " -U " + user_name + " -d alice -p " + port_no)
  i += 1

print "Done loading GPlates geometry"

# Create and alter all the GPlates tables
z = 0
while z < 551:
  current = str(z)
  # Create a cursor for executing queries
  cur = conn.cursor()

  # If the data hasn't been processed yet, uncomment this
  
  query = ("ALTER TABLE reconstructed_" + current + " ADD COLUMN oid SERIAL;"
  "ALTER TABLE reconstructed_" + current + " ADD COLUMN area numeric;"
  "UPDATE reconstructed_" + current + " SET area = ST_Area(geom);"
  "CREATE TABLE reconstructed_" + current + "_processed AS SELECT oid, plateid1 as plateid, name, geom FROM reconstructed_" + current + " WHERE area > 0.3;"
  "CREATE TABLE reconstructed_" + current + "_simple AS SELECT oid, plateid1 as plateid, name, ST_SimplifyPreserveTopology(geom, 0.1) AS geom FROM reconstructed_" + current + ";"
  "DROP TABLE reconstructed_" + current + "_processed;"
  "CREATE TABLE reconstructed_" + current + "_clockwise AS SELECT oid, plateid, name, ST_ForceRHR(geom) AS geom FROM reconstructed_" + current + "_simple;"
  "DROP TABLE reconstructed_" + current + "_simple;"
  """CREATE TABLE reconstructed_""" + current + """_dissolve AS
        SELECT ST_makeValid(ST_SnapToGrid(geom,0.000001)) AS geom, plateid AS plateid, name
        FROM reconstructed_""" + current + """_clockwise;"""
  "ALTER TABLE reconstructed_" + current + "_dissolve ALTER COLUMN plateid TYPE integer;"
  "DROP TABLE reconstructed_" + current + "_clockwise;"
  "CREATE INDEX g" + current + " ON reconstructed_" + current + "_dissolve USING gist (geom);"
  "CREATE INDEX o" + current + " ON reconstructed_" + current + " USING gist (geom);")
  
  #print query

  # Process the data
  try:
    cur.execute(query)
    conn.commit()
    print "Done with " + current
    z += 1
  except NameError as e:
    print e

print "GPlates cleanup done"
