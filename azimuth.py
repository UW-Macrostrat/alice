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

def get_line(year, platea, plateb):

  cur.execute("""
    INSERT INTO distance_azimuth_matrix (platea, plateb, year, shortest_line) (
      SELECT %(platea)s AS platea, %(plateb)s AS plateb, %(year)s AS year, ST_GeomFromText(
        ST_AsText(
          ST_ShortestLine(
              (select geom from merge.reconstructed_%(year)s_merged WHERE plateid = %(platea)s),
              (select geom from merge.reconstructed_%(year)s_merged WHERE  plateid = %(plateb)s)
          )
        )
      ) AS shortest_line
    )
  """, {
    "platea": platea,
    "plateb": plateb,
    "year"  : year
  })
  conn.commit()


def get_lengths(year):
  cur.execute("SELECT id FROM distance_azimuth_matrix  WHERE year = %s", [year])
  plateids = cur.fetchall()

  for plate in plateids:
    cur.execute( """
      UPDATE distance_azimuth_matrix SET distance = (
        SELECT ST_Length_Spheroid(
          (SELECT shortest_line FROM distance_azimuth_matrix WHERE id = %(plate)s),
          'SPHEROID["GRS_1980",6378137,298.257222101]'
        )/1000
      ) WHERE id = %(plate)s""", {"plate": plate[0]})
    conn.commit()
  
  print "Done with lengths for " + str(year)

def get_directions(year):
  cur.execute("SELECT id FROM distance_azimuth_matrix WHERE year = %s", [year])
  plateids = cur.fetchall()

  for plate in plateids:
    
    cur.execute("""
      UPDATE distance_azimuth_matrix SET direction = (
       SELECT degrees( 
          ST_Azimuth(
              ST_StartPoint(line.line),
              ST_EndPoint(line.line)
          )
       ) AS degreesAzimuth
       FROM (
         SELECT shortest_line as line FROM distance_azimuth_matrix WHERE id = %(plate)s
       ) line
      ) WHERE id = %(plate)s""", {"plate": plate[0]})
    conn.commit()
  
  print "Done with directions for year " + str(year)

for year in xrange(0, 551):
  cur.execute("SELECT DISTINCT plateid FROM merge.reconstructed_%(year)s_merged", {"year": year})
  plateids = cur.fetchall()
  for platea in plateids:
    for plateb in plateids:
      if platea[0] != plateb[0]:
        get_line(year, platea[0], plateb[0])

  get_lengths(year)
  get_directions(year)
  print "Done with year " + str(year)

# Create an index on year in `distance_azimuth_matrix`
cur.execute("""
  CREATE INDEX ON distance_azimuth_matrix(year);
  CREATE INDEX ON distance_azimuth_matrix(platea);
  CREATE INDEX ON distance_azimuth_matrix(plateb);
""")
conn.commit()
