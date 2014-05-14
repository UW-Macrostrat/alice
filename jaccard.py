import os
import sys
import psycopg2
import MySQLdb
from config import *

# Connect to the database
try:
  conn = psycopg2.connect(dbname="alice", user=user_name, host=host_name, port=port_no)
except:
  print "Could not connect to database: ", sys.exc_info()[1]
  sys.exit()

# Create a cursor for executing queries
cur = conn.cursor()

try:
  mysql_conn = MySQLdb.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, unix_socket=mysql_unix_socket)
except:
  print "Could not connect to database: ", sys.exc_info()[1]
  sys.exit()

# Cursor for MySQL
mysql_cur = mysql_conn.cursor()

def get_jaccard(pairs, year):

  for index, pair in enumerate(pairs):

    mysql_cur.execute("""

      SELECT distinct genus_name c 
      FROM occ_matrix 
        JOIN paleocoords USING (collection_no) 
      WHERE plate_no=""" + str(pair[0]) + """ 
        AND paleocoords.early_age>= """ + str(year) + """ 
        AND paleocoords.late_age<= """ + str(year) + """

    """)

    platea_genera = mysql_cur.fetchall()
    platea_genera_array = []

    for genus in platea_genera:
      platea_genera_array.append(genus[0])

    mysql_cur.execute("""

      SELECT distinct genus_name c 
      FROM occ_matrix 
        JOIN paleocoords USING (collection_no) 
      WHERE plate_no=""" + str(pair[1]) + """ 
        AND paleocoords.early_age>= """ + str(year) + """ 
        AND paleocoords.late_age<=""" + str(year) + """

    """)

    plateb_genera = mysql_cur.fetchall()
    plateb_genera_array = []

    for genus in plateb_genera:
      plateb_genera_array.append(genus[0])

    cur.execute("""

      UPDATE distance_azimuth_matrix 
        SET (platea_genera, plateb_genera, uunion, intersection) 
        = (%(platea_genera)s, %(plateb_genera)s, %(uunion)s, %(intersection)s)
        WHERE platea = %(platea)s AND plateb = %(plateb)s AND year = %(year)s""", 

      { "platea_genera": len(platea_genera_array), 
        "plateb_genera": len(plateb_genera_array), 
        "uunion": len(list(set(platea_genera_array) | set(plateb_genera_array))), 
        "intersection": len(list(set(platea_genera_array) & set(plateb_genera_array))),
        "platea": str(pair[0]),
        "plateb": str(pair[1]),
        "year": year
      }
    )

    conn.commit()

    # Indicate with year/direction/degree combo was completed
    sys.stdout.write('%s %s\r' % (year, index))
    sys.stdout.flush()

for year in xrange(0, 551):
  cur.execute("SELECT platea, plateb FROM distance_azimuth_matrix WHERE year = " + str(year))
  pairs = cur.fetchall()
  get_jaccard(pairs, year)
  print "----- Done with year " + str(year) + " ------"