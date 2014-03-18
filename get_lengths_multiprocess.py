# Adapted/borrowed from http://stackoverflow.com/a/7556042/1956065
import multiprocessing
import psycopg2
import sys
from config import *

class Consumer(multiprocessing.Process):

  def __init__(self, task_queue, result_queue):
    multiprocessing.Process.__init__(self)
    self.task_queue = task_queue
    self.result_queue = result_queue
    self.pyConn = psycopg2.connect(dbname="gplates", user=user_name, host=host_name, port=port_no)
    self.pyConn.set_isolation_level(0)


  def run(self):
    proc_name = self.name
    while True:
      next_task = self.task_queue.get()
      if next_task is None:
          print 'Tasks complete on this thread'
          self.task_queue.task_done()
          break            
      answer = next_task(connection=self.pyConn)
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
    pyCursor1 = pyConn.cursor()

    # Check if that year has already been done / is being worked on by another process
    pyCursor1.execute(self.check + str(self.year))
    rows = pyCursor1.fetchall()

    # If so, skip it
    if rows[0][0] is not None:
      print "---- Skipping year " + str(self.year) + " ----"

    # Otherwise populate it
    else:
      degree = 89
      while degree > 0:
        self.get_gaps(degree, 'n', self.year, pyConn, pyCursor1)
        self.get_gaps(degree, 's', self.year, pyConn, pyCursor1)

        degree -= 1

      # Populate the equator
      self.get_gaps(0, 'x', self.year, pyConn, pyCursor1)
      print "---- Done with year " + str(self.year) + " ----"


# This corresponds to get_gaps
  def get_gaps(self, degree, direction, year, connection, cursor):
    length_query = """
      SELECT SUM(length) AS sum FROM (
        SELECT ST_Length_Spheroid(
          ST_Intersection(
            (SELECT geom FROM ne_50m_graticules_1 WHERE degrees =  """ + str(degree) + """ AND direction = '""" + direction.upper() + """'), reconstructed_""" + str(self.year) + """_dissolve.geom
          ), 'SPHEROID["GRS_1980",6378137,298.257222101]'
        )/1000 length FROM reconstructed_""" + str(self.year) + """_dissolve
      ) giantSelect
      WHERE length > 0
    """

    cursor.execute(length_query)
    lengths = cursor.fetchall()

    # If something is returned, use that, otherwise default to zero
    if lengths[0][0] is not None:
      total_length = lengths[0][0]
    else:
      total_length = 0

    # Store the length
    self.update_matrix(degree, direction, self.year, total_length, connection, cursor)

    # Indicate with year/direction/degree combo was completed
    print str(year) + " " + direction + str(degree)

  def update_matrix(degree, direction, year, length, connection, cursor):
    cursor.execute("UPDATE length_year_matrix SET " + str(direction) + str(degree) + " = " + str(length) + " WHERE year = " + str(year))
    connection.commit()


if __name__ == '__main__':
  tasks = multiprocessing.JoinableQueue()
  results = multiprocessing.Queue()

  num_consumers = multiprocessing.cpu_count() - 2
  consumers = [Consumer(tasks, results) for i in xrange(num_consumers)]

  for w in consumers:
    w.start()

  for i in xrange(10):
    tasks.put(Task("SELECT n89 FROM length_year_matrix WHERE year = ", i))

  for i in range(num_consumers):
    tasks.put(None)
