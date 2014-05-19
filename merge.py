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

year = 200

def find_groups(year):
  # This keeps track of the groups found
  groups = []

  # This simplifies the process of checking whether or not we have accounted for a given plate
  already_checked = []

  # First, get all plates from the given year
  cur.execute(""" 

    SELECT DISTINCT platea 
    FROM distance_azimuth_matrix 
    WHERE year = """ + str(year) + """
    ORDER BY platea ASC
    
  """)

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
      print "Further processing for ", plate[0]

      # Create a new group for it
      groups.append([plate[0]])

      # The index of the newly created group - used to 
      index = len(groups) - 1

      # Find all of the plates that it touches
      cur.execute("""

        SELECT plateb
        FROM distance_azimuth_matrix
        WHERE year = """ + str(year) + """ AND distance <= 30 AND platea = """ + str(plate[0]) + """
        ORDER BY plateb DESC

      """)

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
            WHERE year = """ + str(year) + """ AND distance <= 30 AND platea = """ + str(to_check[0]) + """
            ORDER BY plateb DESC

          """)

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

    else:
      print "--- Skipping ", plate[0], " ----"

  print groups
  print len(groups), " groups found"