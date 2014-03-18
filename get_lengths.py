import psycopg2
import sys
from config import *

# Connect to the database
try:
  conn = psycopg2.connect(dbname="alice", user=user_name, host=host_name, port=port_no)
except:
  print "Could not connect to database: ", sys.exc_info()[1]
  sys.exit()

# Create a cursor for executing queries
cur = conn.cursor()

# Stores the length of land at a given latitude
def update_matrix(degree, direction, year, length):
  cur.execute("UPDATE length_year_matrix SET " + str(direction) + str(degree) + " = " + str(length) + " WHERE year = " + str(year))
  conn.commit()

# Run spatial query to get length of land at a given latitude
def populate_matrix(degree, direction, year):
  length_query = """
    SELECT SUM(length) AS sum FROM (
      SELECT ST_Length_Spheroid(
        ST_Intersection(
          (SELECT geom FROM ne_50m_graticules_1 WHERE degrees =  """ + str(degree) + """ AND direction = '""" + direction.upper() + """'), reconstructed_""" + str(year) + """_dissolve.geom
        ), 'SPHEROID["GRS_1980",6378137,298.257222101]'
      )/1000 length FROM reconstructed_""" + str(year) + """_dissolve
    ) giantSelect
    WHERE length > 0
  """

  cur.execute(length_query)
  lengths = cur.fetchall()

  # If something is returned, use that, otherwise default to zero
  if lengths[0][0] is not None:
    total_length = lengths[0][0]
  else:
    total_length = 0

  # Store the length
  update_matrix(degree, direction, year, total_length)

  print str(year) + " " + direction + str(degree)


def process(check):
  # Go through each year
  year = 0
  while year < 551:
    
    # Check if that year has already been done / is being worked on by another process
    cur.execute(check + str(year))
    rows = cur.fetchall()

    # If so, skip it
    if rows[0][0] is not None:
      print "---- Skipping year " + str(year) + " ----"
      year += 1

    # Otherwise populate it
    else:
      degree = 89
      while degree > 0:
        populate_matrix(degree, 'n', year)
        populate_matrix(degree, 's', year)

        degree -= 1

      # Populate the equator
      populate_matrix(0, 'x', year)
      print "---- Done with year " + str(year) + " ----"
      year += 1


# ---- Start the process ---- #
process("SELECT n89 FROM length_year_matrix WHERE year = ")


# ---- Quality controoool ---- #
print "---- Checking that all years have been completely filled... ---- "
process("SELECT x0 FROM length_year_matrix WHERE year = ")


print "Done!"