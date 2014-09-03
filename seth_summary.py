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

# Get the data and insert it into the summary table
def get_intersections(degrees, direction, year):
  cur.execute(""" 
    INSERT INTO public.seth_summary (plateid, geom, year, start_lng, start_lat, end_lng, end_lat) (
      SELECT plateid, intersection, %s AS year, ST_X(ST_AsText(ST_StartPoint(intersection))) AS start_lng, ST_Y(ST_AsText(ST_StartPoint(intersection))) AS start_lat, ST_X(ST_AsText(ST_EndPoint(intersection))) AS end_lng, ST_Y(ST_AsText(ST_EndPoint(intersection))) AS end_lng FROM ( 
        SELECT plateid, (st_dump(ST_Intersection(
            (SELECT geom FROM ne_50m_graticules_1 WHERE degrees = %s AND direction = %s), a.geom
          ))).geom as intersection
        FROM chunks.reconstructed_""" + str(year) + """_union a
      ) q where ST_length(intersection) > 0
    );
  """, [year, degrees, direction])

  conn.commit()



# Check to see if we left off somewhere
cur.execute("SELECT max(year) FROM seth_summary")

start_year = cur.fetchall()[0][0]

# If the table is empty, clean up
if start_year < 0 :
  # Drop and recreate the summary table
  cur.execute(""" 
    DROP TABLE IF EXISTS public.seth_summary;
    CREATE TABLE public.seth_summary (
      oid serial PRIMARY KEY,
      plateid integer,
      year integer,
      geom geometry,
      start_lat decimal,
      start_lng decimal,
      end_lat decimal,
      end_lng decimal
    );
  """)

  # Commit the query
  conn.commit()
else :
  start_year -= 1

print "---- Starting with year " + str(start_year) + " ---- "

# For each year between the start year and 550...
for year in xrange(start_year, 551):
  # For each degree between 1 and 89...
  for degree in xrange(1, 90):
    get_intersections(degree, 'N', year)
    get_intersections(degree, 'S', year)

  # Populate the equator
  get_intersections(0, 'XLAT', year)
  print "---- Done with year " + str(year) + " ----"
  year += 1