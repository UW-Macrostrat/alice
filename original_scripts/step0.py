# Step 0 creates the base tables, including GPlates geometry and the graticule

'''
From psql:
 CREATE DATABASE alice;
 \connect alice;
 CREATE EXTENSION postgis;
 CREATE EXTENSION postgis_topology;
'''
import os
import urllib2
from StringIO import StringIO
from zipfile import ZipFile
import psycopg2
from config import *

# Connect to the database
try:
  conn = psycopg2.connect(dbname="alice", user=user_name, host=host_name, port=port_no)
except:
  print "Unable to connect"

# Create a cursor for executing queries
cur = conn.cursor()


'''
i = 0
while i < 551:
  shapefileName = "reconstructed_" + str(i) + ".00Ma.shp"
  os.system("shp2pgsql -s 4326 polygons_550_to_0Ma/Phanerozoic_EarthByte_Coastlines/" + shapefileName + " public." + shapefileName.split(".")[0] + " | psql -h localhost -U john -d alice -p 5439")
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

'''

### Download and import the graticule in PostGIS
# Request the zip file
request = urllib2.urlopen("http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/physical/ne_50m_graticules_1.zip")

print "Downloading graticules from Natural Earth..."

# Extract the contents of the zipfile
with ZipFile(StringIO(request.read())) as zf:
  zf.extractall("graticules")

# Load the one degree graticule into PostGIS
os.system("shp2pgsql -s 4326 graticules/ne_50m_graticules_1.shp | psql -h localhost -U john -d alice -p 5432")

print "One degree graticule shapefile loaded into PostGIS as ne_50m_graticules_1"

# When done, run a VACUUM FULL on alice



# Make a small change to the graticule table
cur.execute("UPDATE ne_50m_graticules_1 SET direction = 'X' WHERE gid = 90")
conn.commit()

# Add a length field to the graticule table
cur.execute("ALTER TABLE ne_50m_graticules_1 ADD column length_km numeric")
conn.commit()

# Populate the length field of the graticule table
cur.execute("""UPDATE ne_50m_graticules_1 SET length_km = ST_Length_Spheroid(geom, 'SPHEROID["GRS_1980",6378137,298.257222101]')""")
conn.commit()