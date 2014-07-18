'''
CREATE TABLE plate_merge_matrix (
  id serial primary key,
  plateid integer not null,
  year integer not null,
  plates integer[]
)
'''
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

def find_groups(year):
  print "Processing year ", year

  # This keeps track of the groups found
  groups = []

  # This simplifies the process of checking whether or not we have accounted for a given plate
  already_checked = []

  # First, get all plates from the given year
  cur.execute(""" 

    SELECT DISTINCT platea 
    FROM distance_azimuth_matrix 
    WHERE year = %s
    ORDER BY platea ASC
    
  """, [year])

  plates = cur.fetchall()

  # Find the plates that each touches
  for plate in plates:

    # Keep track of the plates that need to be checked
    to_check = []
    found = 0

    for groupa in groups:
      if plate[0] in groupa:
        # If we have already put a plate into a group, ignore it
        found = 10

    # If we haven't accounted for this plate, process it
    if found < 1:
      #print "Further processing for ", plate[0]

      # Create a new group for it
      groups.append([plate[0]])

      # The index of the newly created group - used to 
      index = len(groups) - 1

      # Find all of the plates that it touches
      cur.execute("""

        SELECT plateb
        FROM distance_azimuth_matrix
        WHERE year = %s AND distance <= 30 AND platea = %s
        ORDER BY plateb DESC

      """, [year, plate[0]])

      touches = cur.fetchall()

      # For each plate touched, check whether or not it has already been checked
      for each in touches:
        if each[0] not in already_checked:
          to_check.append(each[0])

      # Loop over plates we need to check
      while len(to_check) > 0:
        # If we haven't already checked the plate, add it to the already_checked array
        if to_check[0] not in already_checked:
          already_checked.append(to_check[0])

          # Once again, find all plates that the given plate touches
          cur.execute("""

            SELECT plateb
            FROM distance_azimuth_matrix
            WHERE year = %s AND distance <= 30 AND platea = %s
            ORDER BY plateb DESC

          """, [year, to_check[0]])

          to_check_touches = cur.fetchall()

          # For each touch...
          for x in to_check_touches:
            # If we haven't seen it before, add it to the to_check array 
            if x[0] not in already_checked and x[0] not in to_check:
              to_check.append(x[0])

            # If it's not already in the current grouping, add it
            if x[0] not in groups[index]:
              groups[index].append(x[0])

          # Remove it from the to_check array
          to_check.remove(to_check[0])

   # else:
      #print "--- Skipping ", plate[0], " ----"

  print len(groups), " groups found"

  # Create table to hold uninoned geometry
  cur.execute("""
    DROP TABLE IF EXISTS reconstructed_""" + str(year) + """_union;
    CREATE TABLE reconstructed_""" + str(year) + """_union (
      id serial primary key,
      plateid integer not null,
      geom geometry
    )
  """)
  conn.commit()

  for index, group in enumerate(groups):

    # Record which plates belong to which feature
    cur.execute("""
      INSERT INTO plate_merge_matrix (plateid, year, plates)
      VALUES (%(plateid)s, %(year)s, %(plates)s)
    """, {
          "plateid": index,
          "year": year,
          "plates": group
        }
    )
    conn.commit()

    # Create a temp table of rough unioned geometry
    cur.execute("""
      DROP TABLE IF EXISTS temp_union;
      CREATE TABLE temp_union AS
      SELECT ST_Union(geom) AS geom 
      FROM (
        SELECT * FROM (
         SELECT (ST_Dump(geom)).geom AS geom, plateid 
              FROM reconstructed_""" + str(year) + """_merged rm
              ORDER BY plateid asc
        ) w 
        WHERE GEOMETRYTYPE(geom) = 'POLYGON'
        AND plateid IN (
          SELECT unnest(plates) FROM plate_merge_matrix WHERE plateid = %(plateid)s AND year = %(year)s
        )
      ) q;
    """, {"plateid": index, "year": year})
    conn.commit()

    # Dump all rings with area > 20
    cur.execute("""
      DROP TABLE IF EXISTS temp_rings;
      CREATE TABLE temp_rings AS SELECT row_number() OVER() AS id, * FROM (
        SELECT ST_Area((ST_DumpRings((ST_Dump(geom)).geom)).geom) AS area, (ST_DumpRings((ST_Dump(geom)).geom)).geom AS geom 
        FROM temp_union
      ) q WHERE area > 20
      ORDER BY area DESC;
    """)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM temp_rings")
    num_records = cur.fetchall()

    if num_records[0][0] > 1:
      i = 2
      while i <= num_records[0][0]:
        if i == 2:
          # Insert new row
          cur.execute("""
            INSERT INTO temp_rings (id, geom) VALUES (
              99999, 
              (SELECT ST_Union(ST_SymDifference(
                (SELECT geom FROM temp_rings WHERE id = 1), 
                (SELECT geom FROM temp_rings WHERE id = %(id)s)
              )))
            )
          """, {"id": i})
          conn.commit()
        else:
          # Update existing row
          cur.execute("""
            UPDATE temp_rings SET geom = (SELECT 
            ST_Union(ST_SymDifference(
              (SELECT geom FROM temp_rings WHERE id = 99999), 
              (SELECT geom FROM temp_rings WHERE id = %(id)s)
            )) FROM temp_rings) WHERE id = 99999 
          """, {"id": i})
          conn.commit()
        i = i + 1

      # Once done rebuilding the geometry, insert it into the final table
      cur.execute("""
        INSERT INTO reconstructed_""" + str(year) + """_union (plateid, geom) (
          SELECT %(index)s AS plateid, geom
          FROM temp_rings
          WHERE id = 99999
        );

      """, {"index": index})
      conn.commit()

    elif num_records[0][0] == 1:
      cur.execute("""
        INSERT INTO reconstructed_""" + str(year) + """_union (plateid, geom) (
          SELECT %(index)s AS plateid, geom
          FROM temp_rings
          WHERE id = 1
        );

      """, {"index": index})
      conn.commit()

    else:
      cur.execute("""
        INSERT INTO reconstructed_""" + str(year) + """_union (plateid, geom) (
          SELECT %(index)s AS plateid, geom
          FROM temp_union
        );

      """, {"index": index})
      conn.commit()

## Process - change to however many years need to be processed
for year in xrange(0, 1):
  find_groups(year)