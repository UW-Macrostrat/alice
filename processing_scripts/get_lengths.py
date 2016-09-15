import psycopg2
import sys
from config import *
import numpy as np

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
  if degree.is_integer():
    deg = str(int(degree))
  else:
    deg = str(degree).replace('.', '_')
  cur.execute("UPDATE burwell_rotated.latitudinal_area SET " + str(direction) + deg + " = %(length)s WHERE year = %(year)s", {
    "year": year,
    "length": length
    })
  conn.commit()


def makeLinestring(direction, coord) :
  lngs = np.arange(-179.5, 180, 0.1)
  coordinates = []
  linestring = "LINESTRING("
  if direction == "n":
    for lng in lngs:
      coordinates.append((str(lng) + " " + str(coord)))

    linestring += ", ".join(coordinates) + ")"

  elif direction == "s":
    for lng in lngs:
      coordinates.append((str(lng) + " -" + str(coord)))

    linestring += ", ".join(coordinates) + ")"
  
  elif direction == "xlat":
    for lng in lngs:
      coordinates.append((str(lng) + " " + str(coord)))

    linestring += ", ".join(coordinates) + ")"

  else:
    print "huh?"

  return linestring

# Run spatial query to get length of land at a given latitude
def populate_matrix(degree, direction, year):
  linestring = makeLinestring(direction, degree)
  cur.execute("""
    SELECT SUM(length) AS sum FROM (
      SELECT ST_Length_Spheroid(
        ST_Intersection(
          (ST_GeomFromText(%(linestring)s, 4326)), ST_Union(burwell_rotated.""" + str(year) + """.geom)
        ), 'SPHEROID["GRS_1980",6378137,298.257222101]'
      )/1000 length FROM burwell_rotated.""" + str(year) + """
    ) giantSelect
    WHERE length > 0
  """, { 'linestring': linestring })
  lengths = cur.fetchall()

  # If something is returned, use that, otherwise default to zero
  if lengths[0][0] is not None:
    total_length = lengths[0][0]
  else:
    total_length = 0

  # Store the length
  update_matrix(degree, direction, year, total_length)

  print str(year) + " " + direction + str(degree)


def process():
  # Go through each year
  periods = ["meow_ecos","cambrian_rotated", "ordovician_rotated", "silurian_rotated", "devonian_rotated", "carboniferous_rotated", "permian_rotated", "triassic_rotated", "jurassic_rotated", "cretaceous_rotated", "paleogene_rotated", "neogene_rotated", "quaternary_rotated"]

  for period in periods:
    cur.execute('INSERT INTO burwell_rotated.latitudinal_area (year) VALUES (%(year)s)', { "year": period})
    conn.commit()
    degree = 89.0
    while degree > 0:
      populate_matrix(degree, 'n', period)
      populate_matrix(degree, 's', period)

      degree -= 0.5

    # Populate the equator
    populate_matrix(0.0, 'xlat', period)
    print "---- Done with year " + str(period) + " ----"



process()


print "Done!"
