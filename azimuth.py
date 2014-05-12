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
  query = """
    SELECT ST_AsText(
      ST_ShortestLine(
          (select geom from reconstructed_""" + str(year) + """_merged WHERE plateid = """ + str(platea) + """),
          (select geom from reconstructed_""" + str(year) + """_merged WHERE  plateid = """ + str(plateb) + """)
      )
    ) AS line
  """

  cur.execute(query)
  results = cur.fetchall()

  cur.execute("INSERT INTO distance_azimuth_matrix (platea, plateb, year, shortest_line) VALUES(" + str(platea) + ", " + str(plateb) + ", " + str(year) + ", ST_GeomFromText('" + results[0][0] + "'))")
  conn.commit()


def get_lengths(year):
  cur.execute("SELECT id FROM distance_azimuth_matrix  WHERE year = " + str(year))
  plateids = cur.fetchall()

  for plate in plateids:
    query = """
      UPDATE distance_azimuth_matrix SET distance = (
        SELECT ST_Length_Spheroid(
          (SELECT shortest_line FROM distance_azimuth_matrix_lat WHERE id = """ + str(plate[0]) + """),
          'SPHEROID["GRS_1980",6378137,298.257222101]'
        )/1000
      ) WHERE id = """ + str(plate[0])
    
    cur.execute(query)
    conn.commit()
  
  print "Done with lengths for " + str(year)

def get_directions(year):
  cur.execute("SELECT id FROM distance_azimuth_matrix WHERE year = " + str(year))
  plateids = cur.fetchall()

  for plate in plateids:
    query = """
      UPDATE distance_azimuth_matrix SET direction = (
       SELECT degrees( 
          ST_Azimuth(
              ST_StartPoint(line.line),
              ST_EndPoint(line.line)
          )
       ) AS degreesAzimuth
       FROM (
         SELECT shortest_line as line FROM distance_azimuth_matrix WHERE id = """ + str(plate[0]) + """
       ) line
      ) WHERE id = """ + str(plate[0])
    
    cur.execute(query)
    conn.commit()
  
  print "Done with directions for year " + str(year)

for year in xrange(0, 551):
  cur.execute("SELECT DISTINCT plateid FROM reconstructed_" + str(year) + "_merged")
  plateids = cur.fetchall()
  for platea in plateids:
    for plateb in plateids:
      if platea[0] != plateb[0]:
        get_line(year, platea[0], plateb[0])

  get_lengths(year)
  get_directions(year)
  print "Done with year " + str(year)

