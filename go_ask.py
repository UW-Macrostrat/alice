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

# Import the shapefiles into PostGIS 
for year in xrange(0, 551):
  current = str(year)
  shapefileName = "reconstructed_" + current + ".00Ma.shp"

  cur.execute("DROP TABLE IF EXISTS reconstructed_" + current + "_merged")
  conn.commit() 

  os.system("shp2pgsql -s 4326 polygons_550_to_0Ma/Phanerozoic_EarthByte_ContinentalRegions/" + shapefileName + " public." + shapefileName.split(".")[0] + " | psql -h " + host_name + " -U " + user_name + " -d alice -p " + str(port_no))

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
  "DROP TABLE reconstructed_" + current + ";"
  """CREATE TABLE reconstructed_""" + current + """_merged AS
        SELECT ST_Union(ST_MakeValid(ST_SnapToGrid(geom, 0.0001))) AS geom, plateid
        FROM reconstructed_""" + current + """_fixed
        GROUP BY plateid;

    CREATE INDEX in""" + current + """ ON reconstructed_""" + current + """_merged USING gist (geom);

    DROP TABLE reconstructed_""" + current + """_fixed;"""
  )
  
  # Process the data
  try:
    cur.execute(query)
    conn.commit()
    print "Done with " + current
  except NameError as e:
    print e


print "Done loading and processing GPlates geometry"
