import os
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

def get_distance(year):
  # Get distance from equator and prime meridian
  '''
  cur.execute("""
    INSERT INTO centroid_matrix (year, plateid, distance_equator, distance_meridian) 
      (SELECT %s AS year, plateid, ST_Distance_Spheroid(
        ST_Centroid(geom),
        (SELECT geom FROM ne_50m_graticules_1 WHERE direction = 'XLAT'),
        'SPHEROID["GRS_1980",6378137,298.257222101]'
      )/1000 AS distance_equator, 
      ST_Distance_Spheroid(
        ST_Centroid(geom),
        (SELECT geom FROM ne_50m_graticules_1 WHERE direction = 'XLNG'),
        'SPHEROID["GRS_1980",6378137,298.257222101]'
      )/1000 AS distance_meridian FROM reconstructed_""" + str(year) + """_merged
    )
  """, [year])
'''
  cur.execute("""
    INSERT INTO centroid_matrix (year, plateid, distance_equator, distance_meridian, max_lat, min_lat) 
      (SELECT %s AS year, plateid, ST_Y((ST_Centroid(geom))), ST_X((ST_Centroid(geom))), ST_ymax(geom) AS max_lat, ST_ymin(geom) AS min_lat
      FROM reconstructed_""" + str(year) + """_merged)
  """, [year])

  conn.commit()

# Iterate over each year
for year in xrange(0, 551):
  get_distance(year)
  print "----- Done with year " + str(year) + " ------"

cur.execute("""
  CREATE INDEX ON centroid_matrix (plateid);
  CREATE INDEX ON centroid_matrix (year);
""")
conn.commit()

print "Done!"
