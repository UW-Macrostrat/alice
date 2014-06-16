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


# Stores the number of plates crossed
def update_matrix(degree, direction, year, table, count):
  cur.execute("UPDATE " + str(table) + " SET " + str(direction) + str(degree) + " = " + str(count) + " WHERE year = " + str(year))
  conn.commit()


def get_gaps(degree, direction, year):
  # Returns an array, where each row is a plate crossed and the total length of that crossing
  get_gap_lengths = """
    SELECT ST_Length_Spheroid(geometry, 'SPHEROID["GRS_1980",6378137,298.257222101]')/1000 AS gap_length FROM (
      SELECT (ST_Dump(
          (SELECT ST_DIFFERENCE((SELECT geom FROM ne_50m_graticules_1 WHERE degrees =  """ + str(degree) + """ AND direction = '""" + direction.upper() + """'), ST_UNION(geom)) 
        FROM reconstructed_""" + str(year) + """_dissolve)
      )).geom AS geometry
    ) giantselect
  """

  cur.execute(get_gap_lengths)
  gap_lengths_tuples = cur.fetchall()
  gap_lengths = []

  # Each row comes back as a tuple, so we'll simplify into a flat list for ease of counting
  for each in gap_lengths_tuples:
    gap_lengths.append(each[0])

  # If there is 1 gap, but it's very small, say that land covers that latitude
  if len(gap_lengths) == 1:
    if  gap_lengths[0] < 2:
      gap_lengths = []

  # In KM
  counts = {
    "250": [gap for gap in gap_lengths if gap > 250],
    "500": [gap for gap in gap_lengths if gap > 500],
    "1000": [gap for gap in gap_lengths if gap > 1000],
    "1500": [gap for gap in gap_lengths if gap > 1500]
  }

  # Record the gap counts
  for threshold, gaps in counts.iteritems():
    update_matrix(degree, direction, year, "gaps" + threshold, len(gaps))

  # Indicate with year/direction/degree combo was completed
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
        get_gaps(degree, 'n', year)
        get_gaps(degree, 's', year)

        degree -= 1

      # Populate the equator
      get_gaps(0, 'x', year)
      print "---- Done with year " + str(year) + " ----"
      year += 1


# ---- Start the process ---- #
process("SELECT n89 FROM gaps250 WHERE year = ")


# ---- Quality controoool ---- #
print "---- Checking that all years have been completely filled... ---- "
process("SELECT x0 FROM gaps250 WHERE year = ")


print "Done!"