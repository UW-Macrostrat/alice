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

  cur.execute("DROP TABLE IF EXISTS merge.reconstructed_" + current + "_merged; DROP TABLE IF EXISTS orig.reconstructed_" + current + ";")
  conn.commit() 

  os.system("shp2pgsql -s 4326 polygons_550_to_0Ma/Phanerozoic_EarthByte_ContinentalRegions/" + shapefileName + " orig." + shapefileName.split(".")[0] + " | psql -h " + host_name + " -U " + user_name + " -d alice -p " + str(port_no))

  # Process the data
  query = """
    ALTER TABLE orig.reconstructed_%(year)s ADD COLUMN oid SERIAL;
    UPDATE orig.reconstructed_%(year)s SET name = 'valid_continental' WHERE objectid_1 = 107;
    UPDATE orig.reconstructed_%(year)s SET name = 'valid_continental' WHERE objectid_1 = 144;
    UPDATE orig.reconstructed_%(year)s SET name = 'valid_continental' WHERE objectid_1 = 145;
    ALTER TABLE orig.reconstructed_%(year)s ADD COLUMN area numeric;
    UPDATE orig.reconstructed_%(year)s SET area = ST_Area(geom);
    DELETE FROM orig.reconstructed_%(year)s WHERE area < 0.3;
    DELETE FROM orig.reconstructed_%(year)s WHERE name IS NULL;
    ALTER TABLE orig.reconstructed_%(year)s ADD COLUMN geomsimp GEOMETRY;
    UPDATE orig.reconstructed_%(year)s SET geomsimp = ST_SimplifyPreserveTopology(geom, 0.1);
    UPDATE orig.reconstructed_%(year)s SET geomsimp = ST_ForceRHR(geomsimp);
    UPDATE orig.reconstructed_%(year)s SET geomsimp = ST_makeValid(ST_SnapToGrid(geomsimp,0.000001));
    CREATE INDEX ON orig.reconstructed_%(year)s USING gist (geomsimp);

    CREATE TABLE merge.reconstructed_%(year)s_merged AS
        SELECT ST_Union(ST_makeValid(ST_SnapToGrid(geomsimp,0.000001))) AS geom, plateid1 AS plateid, 1 AS land
        FROM orig.reconstructed_%(year)s
        GROUP BY plateid;

    CREATE INDEX ON merge.reconstructed_%(year)s_merged USING gist (geom);

    ALTER TABLE merge.reconstructed_%(year)s_merged ADD COLUMN geomsimp GEOMETRY;
    UPDATE merge.reconstructed_%(year)s_merged SET geomsimp = ST_makeValid(ST_SnapToGrid(geom, 0.01)); 

  """ % {"year": current}
  
  # Process the data
  try:
    cur.execute(query)
    conn.commit()
    print "Done with " + current
  except NameError as e:
    print e


print "Done loading and processing GPlates geometry"
