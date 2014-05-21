import multiprocessing
import urllib2
import json
from jaccard_multiprocessor import *


if __name__ == '__main__':
  tasks = multiprocessing.JoinableQueue()
  results = multiprocessing.Queue()

  num_processors = multiprocessing.cpu_count() - cpus_free
  processors = [Processor(tasks, results) for i in xrange(num_processors)]

  for each in processors:
    each.start()
  
  # Get stage midpoints, if applicable
  '''
  midpoints = []
  time_data = json.load(urllib2.urlopen('http://paleobiodb.org/data1.1/intervals/list.json?scale=1&order=older&max_ma=4000'))
  for interval in time_data['records']:
    if interval['lvl'] == 5:
      midpoint = int((interval['lag'] + interval['eag'])/2)
      if midpoint not in midpoints:
        midpoints.append(midpoint)
  '''

  # Set the range to whatever year you want to go up to (551 is the max)
  for i in xrange(551):
  #for i in midpoints:
    tasks.put(Task("SELECT sum(uunion) FROM distance_azimuth_matrix WHERE year = ", i))

  for i in range(num_processors):
    tasks.put(None)