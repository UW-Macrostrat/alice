# Adapted/borrowed from http://stackoverflow.com/a/7556042/1956065
import multiprocessing
import psycopg2
from config import *

class Processor(multiprocessing.Process):

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
  def __init__(self, check, year, type):
    self.check = check
    self.year = year
    self.type = type

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
        if self.type == "lengths":
          self.get_length_data(degree, 'n', self.year, pyConn, pyCursor1)
          self.get_length_data(degree, 's', self.year, pyConn, pyCursor1)

          degree -= 1
        else:
          self.get_gap_data(degree, 'n', self.year, pyConn, pyCursor1)
          self.get_gap_data(degree, 's', self.year, pyConn, pyCursor1)

          degree -= 1

      # Populate the equator]
      if self.type == "lengths":
        self.get_length_data(0, 'x', self.year, pyConn, pyCursor1)
      else:
        self.get_gap_data(0, 'x', self.year, pyConn, pyCursor1)

      print "---- Done with year " + str(self.year) + " ----"
  
  # Method for getting length
  def get_length_data(self, degree, direction, year, connection, cursor):
    length_query = """
      SELECT SUM(length) AS sum FROM (
        SELECT ST_Length_Spheroid(
          ST_Intersection(
            (SELECT geom FROM ne_50m_graticules_1 WHERE degrees =  """ + str(degree) + """ AND direction = '""" + direction.upper() + """'), reconstructed_""" + str(year) + """_fixed.geom
          ), 'SPHEROID["GRS_1980",6378137,298.257222101]'
        )/1000 length FROM reconstructed_""" + str(year) + """_fixed
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
    self.update_matrix(degree, direction, year, "length_year_matrix", total_length, connection, cursor)

    # Indicate with year/direction/degree combo was completed
    print str(year) + " " + direction + str(degree)
  
  # Method for getting gap data
  def get_gap_data(self, degree, direction, year, connection, cursor):
    get_gap_lengths = """
      SELECT ST_Length_Spheroid(geometry, 'SPHEROID["GRS_1980",6378137,298.257222101]')/1000 AS gap_length FROM (
        SELECT (ST_Dump(
            (SELECT ST_DIFFERENCE((SELECT geom FROM ne_50m_graticules_1 WHERE degrees =  """ + str(degree) + """ AND direction = '""" + direction.upper() + """'), ST_UNION(geom)) 
          FROM reconstructed_""" + str(self.year) + """_fixed)
        )).geom AS geometry
      ) giantselect
    """

    cursor.execute(get_gap_lengths)
    gap_lengths_tuples = cursor.fetchall()
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
      self.update_matrix(degree, direction, self.year, "gaps" + threshold, len(gaps), connection, cursor)

    # Indicate with year/direction/degree combo was completed
    print str(year) + " " + direction + str(degree)


  def update_matrix(self, degree, direction, year, table, data, connection, cursor):
    cursor.execute("UPDATE " + str(table) + " SET " + str(direction) + str(degree) + " = " + str(data) + " WHERE year = " + str(year))
    connection.commit()
