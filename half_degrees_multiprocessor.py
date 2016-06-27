# Adapted/borrowed from http://stackoverflow.com/a/7556042/1956065
import multiprocessing
import psycopg2
from psycopg2.extensions import AsIs
import sys
import numpy as np

class Processor(multiprocessing.Process):

  def __init__(self, task_queue, result_queue):
    multiprocessing.Process.__init__(self)
    self.task_queue = task_queue
    self.result_queue = result_queue
    self.pyConn = psycopg2.connect(dbname="alice", user="john", host="localhost", port="5432")
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
  def __init__(self, coord_type, direction, coord, year):
    self.coord_type = coord_type
    self.direction = direction
    self.coord = coord
    self.year = year
    self.line_step = 0.1

  # Acts as the controller for a given year
  def __call__(self, connection=None):
    pyConn = connection
    pyCursor1 = pyConn.cursor()

    table = "length_year_matrix_" + self.coord_type + "_half"
    line = self.makeLinestring(self.coord_type, self.direction, self.coord, self.line_step)
    field = self.direction

    if not self.coord.is_integer():
      field += str(int(self.coord)) + "_5"
    else :
      field += str(int(self.coord))

    pyCursor1.execute(""" 
      UPDATE %(insert_table)s 
        SET %(coordinate)s = subquery.sum
        FROM (
          SELECT SUM(length) AS sum FROM (
            SELECT ST_Length_Spheroid(
              ST_Intersection(
                ST_GeomFromText(%(linestring)s, 4326), geom
              ), 'SPHEROID["GRS_1980",6378137,298.257222101]'
            )/1000 length FROM chunks_can.reconstructed_%(table_year)s
          ) giantSelect
        ) AS subquery WHERE year = %(year)s

    """, {
      "insert_table": AsIs(table),
      "coordinate": AsIs(field),
      "linestring": line,
      "table_year": AsIs(self.year),
      "year": self.year
    })

    pyConn.commit()

    sys.stdout.write('%s %s %s\r' % (self.year, self.direction, self.coord))
    sys.stdout.flush()
  

  def makeLinestring(self, coord_type, direction, coord, line_step) :
    if coord_type == "lat":
      if direction == "n":
        lngs = np.arange(-179.5, 180, line_step)
        coordinates = []
        linestring = "LINESTRING("
        for lng in lngs:
          coordinates.append((str(lng) + " " + str(coord)))

        linestring += ", ".join(coordinates) + ")"

      elif direction == "s":
        lngs = np.arange(-179.5, 180, line_step)
        coordinates = []
        linestring = "LINESTRING("
        for lng in lngs:
          coordinates.append((str(lng) + " -" + str(coord)))

        linestring += ", ".join(coordinates) + ")"
      
      elif direction == "xlat":
        lngs = np.arange(-179.5, 180, line_step)
        coordinates = []
        linestring = "LINESTRING("
        for lng in lngs:
          coordinates.append((str(lng) + " " + str(coord)))

        linestring += ", ".join(coordinates) + ")"

      else:
        print "huh?"

    elif coord_type == "lng":
      if direction == "w" :
        lats = np.arange(-89.5, 90, line_step)
        coordinates = []
        linestring = "LINESTRING("
        for lat in lats:
          coordinates.append("-" + str(coord) + " " + str(lat))

        linestring += ", ".join(coordinates) + ")"

      elif direction == "e":
        lats = np.arange(-89.5, 90, line_step)
        coordinates = []
        linestring = "LINESTRING("
        for lat in lats:
          coordinates.append(str(coord) + " " + str(lat))

        linestring += ", ".join(coordinates) + ")"

      elif direction == "xlng":
        lats = np.arange(-89.5, 90, line_step)
        coordinates = []
        linestring = "LINESTRING("
        for lat in lats:
          coordinates.append(str(coord) + " " + str(lat))

        linestring += ", ".join(coordinates) + ")"

      else :
        print "huh?"

    return linestring

