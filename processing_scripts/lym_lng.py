# Adapted/borrowed from http://stackoverflow.com/a/7556042/1956065
import multiprocessing
import psycopg2
from psycopg2.extensions import AsIs
import sys
from credentials import *

class Processor(multiprocessing.Process):

  def __init__(self, task_queue, result_queue):
    multiprocessing.Process.__init__(self)
    self.task_queue = task_queue
    self.result_queue = result_queue
    self.pyConn = psycopg2.connect(dbname="alice", user=pg_user, host=pg_host, port=pg_port)
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
  def __init__(self, year):
    self.year = year

  # Acts as the controller for a given year
  def __call__(self, connection=None):
    pyConn = connection
    pyCursor1 = pyConn.cursor()

    pyCursor1.execute("""
        INSERT INTO plate_length_year_can_lng (year, plateid, coord, the_length)
        SELECT %(year)s AS year, plateid, coord, ST_Length_Spheroid(
        	ST_Intersection(
        		ST_SetSRID(half_degree_lng.geom, 4326),
        	 	r.geom
        	 )
        	 , 'SPHEROID["GRS_1980",6378137,298.257222101]')/1000 the_length
        FROM merge.reconstructed_""" + str(self.year) + """_merged r, half_degree_lng
        WHERE plateid IN (
        	SELECT distinct plateid FROM merge.reconstructed_550_merged
        );
    """, {
        "year": self.year
    })
    pyConn.commit()

    # Indicate which year was completed
    sys.stdout.write('%s\r' % (self.year,))
    sys.stdout.flush()
