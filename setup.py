# Sets up the database for processing

import os
import sys
import psycopg2
from config import *

# Create the database 'alice' and some tables
os.system("psql --set 'user='" + user_name + " -p " + str(port_no) + " -U " + user_name + " -f alice.sql")



# Connect to the database
try:
  conn = psycopg2.connect(dbname="alice", user=user_name, host=host_name, port=port_no)
except:
  print "Could not connect to database: ", sys.exc_info()[1]
  sys.exit()

# Create a cursor for executing queries
cur = conn.cursor()

def create_lookup(): 
  cur.execute("DROP TABLE IF EXISTS name_lookup")
  conn.commit()
  cur.execute(""" 
    CREATE TABLE name_lookup(
      plateid     integer,
      names       text
    ) 
  """)
  conn.commit()

  cur.execute("SELECT DISTINCT plateid FROM reconstructed_0_fixed")
  plateids = cur.fetchall()

  i = 0
  while i < len(plateids):
    cur.execute("SELECT name FROM reconstructed_0_fixed WHERE plateid = " + str(plateids[i][0]))
    plates = cur.fetchall()

    names = []
    j = 0
    while j < len(plates):
      if plates[j][0] not in names:
        names.append(plates[j][0])
      j += 1

    cur.execute("INSERT INTO name_lookup VALUES(%(plateid)s, %(names)s)", {"plateid": plateids[i][0], "names": ', '.join(names) })
    conn.commit()
    i += 1

# Import the shapefiles into PostGIS   
i = 0
while i < 551:
  shapefileName = "reconstructed_" + str(i) + ".00Ma.shp"
  os.system("shp2pgsql -s 4326 polygons_550_to_0Ma/Phanerozoic_EarthByte_ContinentalRegions/" + shapefileName + " public." + shapefileName.split(".")[0] + " | psql -h " + host_name + " -U " + user_name + " -d alice -p " + str(port_no))
  i += 1

print "Done loading GPlates geometry"

# Create and alter all the GPlates tables
z = 0
while z < 551:
  current = str(z)
  # Create a cursor for executing queries
  cur = conn.cursor()

  # Process the data
  query = ("ALTER TABLE reconstructed_" + current + " ADD COLUMN oid SERIAL;"
  "UPDATE reconstructed_" + current + " SET name = 'valid_continental' WHERE objectid_1 = 107;"
  "UPDATE reconstructed_" + current + " SET name = 'valid_continental' WHERE objectid_1 = 144;"
  "UPDATE reconstructed_" + current + " SET name = 'valid_continental' WHERE objectid_1 = 145;"
  "ALTER TABLE reconstructed_" + current + " ADD COLUMN area numeric;"
  "UPDATE reconstructed_" + current + " SET area = ST_Area(geom);"
  "CREATE TABLE reconstructed_" + current + "_processed AS SELECT oid, plateid1 as plateid, name, geom FROM reconstructed_" + current + " WHERE area > 0.3 AND name IS NOT NULL;"
  "CREATE TABLE reconstructed_" + current + "_simple AS SELECT oid, plateid1 as plateid, name, objectid_1 as objectid, ST_SimplifyPreserveTopology(geom, 0.1) AS geom FROM reconstructed_" + current + ";"
  "DROP TABLE reconstructed_" + current + "_processed;"
  "CREATE TABLE reconstructed_" + current + "_clockwise AS SELECT oid, plateid, name, objectid, ST_ForceRHR(geom) AS geom FROM reconstructed_" + current + "_simple;"
  "DROP TABLE reconstructed_" + current + "_simple;"
  """CREATE TABLE reconstructed_""" + current + """_fixed AS
        SELECT ST_makeValid(ST_SnapToGrid(geom,0.000001)) AS geom, plateid AS plateid, name, objectid
        FROM reconstructed_""" + current + """_clockwise WHERE name IS NOT NULL;"""
  "ALTER TABLE reconstructed_" + current + "_fixed ALTER COLUMN plateid TYPE integer;"
  "DROP TABLE reconstructed_" + current + "_clockwise;"
  "CREATE INDEX g" + current + " ON reconstructed_" + current + "_fixed USING gist (geom);"
  "DROP TABLE reconstructed_" + current + ";")

  # Process the data
  try:
    cur.execute(query)
    conn.commit()
    print "Done with " + current
    z += 1
  except NameError as e:
    print e

# Create a name lookup table for use later
create_lookup()

# Dissolve the geometry on plateid
z = 0
while z < 551:
  current = str(z)
  # Create a cursor for executing queries
  cur = conn.cursor()
  query = (""" 
    CREATE TABLE reconstructed_""" + current + """_merged AS
        SELECT ST_Union(ST_Buffer(geom, 0.0000001)) AS geom, plateid
        FROM reconstructed_""" + current + """_fixed
        GROUP BY plateid;

    CREATE INDEX in""" + current + """ ON reconstructed_""" + current + """_merged USING gist (geom);

    DROP TABLE reconstructed_""" + current + """_fixed;
  """)

  try:
    cur.execute(query)
    conn.commit()
    print "Created merged " + current
    z += 1
  except NameError as e:
    print e

print "GPlates cleanup done"
