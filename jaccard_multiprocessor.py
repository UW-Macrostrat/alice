# Adapted/borrowed from http://stackoverflow.com/a/7556042/1956065
import multiprocessing
import psycopg2
import sys
from config import *

class Processor(multiprocessing.Process):

  def __init__(self, task_queue, result_queue):
    multiprocessing.Process.__init__(self)
    self.task_queue = task_queue
    self.result_queue = result_queue
    self.connection = psycopg2.connect(dbname="alice", user=user_name, host=host_name, port=port_no)
    self.connection.set_isolation_level(0)


  def run(self):
    proc_name = self.name
    while True:
      next_task = self.task_queue.get()
      if next_task is None:
          print 'Tasks complete on this thread'
          self.task_queue.task_done()
          break            
      answer = next_task(connection=self.connection)
      self.task_queue.task_done()
      self.result_queue.put(answer)
    return

class Task(object):
  # Assign check and year when initialized
  def __init__(self, check, year):
    self.check = check
    self.year = year

  # Acts as the controller for a given year
  def __call__(self, connection=None):
    pyConn = connection
    cursor = pyConn.cursor()

    # Check if that year has already been done / is being worked on by another process
    cursor.execute(self.check + str(self.year))
    rows = cursor.fetchall()

    # If so, skip it
    if rows[0][0] is not None:
      print "---- Skipping year " + str(self.year) + " ----"
      return
    else:
      self.get_jaccard(self.year, pyConn, cursor)

      print "---- Done with year " + str(self.year) + " ----"
      return


  def get_jaccard(self, year, pyConn, cursor):
    cursor.execute("SELECT platea, plateb FROM distance_azimuth_matrix WHERE year = %s", [year])
    pairs = cursor.fetchall()
    for index, pair in enumerate(pairs):

      cursor.execute("""
        SELECT array_length(ARRAY (
            SELECT UNNEST(a1)
            UNION
            SELECT UNNEST(a2)
        ), 1) AS uunion,
        array_length(ARRAY (
            SELECT UNNEST(a1)
            INTERSECT
            SELECT UNNEST(a2)
        ), 1) AS intersection
        FROM  (
            SELECT (SELECT genera FROM plate_genera WHERE plateid = %(platea)s AND year = %(year)s) AS a1,
            (SELECT genera FROM plate_genera WHERE plateid = %(plateb)s AND year = %(year)s) AS a2
        ) stats
      """, 

        { "platea": pair[0],
          "plateb": pair[1],
          "year"  : year
        }
      )

      stats = cursor.fetchall()
      for stat in stats[0]:
        if stat is None:
          stat = 0, 2

      cursor.execute("""

        UPDATE distance_azimuth_matrix 
          SET (uunion, intersection) 
          = (%(uunion)s, %(intersection)s)
          WHERE platea = %(platea)s AND plateb = %(plateb)s AND year = %(year)s""", 

        { "uunion": stats[0][0], 
          "intersection": stats[0][1],
          "platea": pair[0],
          "plateb": pair[1],
          "year": year
        }
      )

      pyConn.commit()

      # Indicate with year/direction/degree combo was completed
      sys.stdout.write('%s %s\r' % (year, index))
      sys.stdout.flush()
