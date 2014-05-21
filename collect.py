import multiprocessing
import argparse
from multiprocessor import *

parser = argparse.ArgumentParser(
  description="Populate the result matrices of Alice",
  epilog="Example usage: python collect.py -t gaps")

parser.add_argument("-t", "--type", dest="type",
  default="lengths", type=str, required=True,
  help="Type of data to collect. Can be either 'lengths' or 'gaps'.")

parser.add_argument("-ll", "--latlng", dest="ll",
  default="lat", type=str, required=True,
  help="Use either latitude or longitude. Can be either 'lat' or 'lng'.")

arguments = parser.parse_args()

if __name__ == '__main__':
  tasks = multiprocessing.JoinableQueue()
  results = multiprocessing.Queue()

  num_processors = multiprocessing.cpu_count() - cpus_free
  processors = [Processor(tasks, results) for i in xrange(num_processors)]

  for each in processors:
    each.start()
  
  # Set the range to whatever year you want to go up to (551 is the max)
  for i in xrange(551):
    if arguments.type == "gaps":
      if arguments.ll == "lat":
        tasks.put(Task("SELECT n89 FROM gaps250_" + arguments.ll + " WHERE year = ", i, "gaps", arguments.ll))
      else:
        tasks.put(Task("SELECT e180 FROM gaps250_" + arguments.ll + " WHERE year = ", i, "gaps", arguments.ll))
    else:
      if arguments.ll == "lat":
        tasks.put(Task("SELECT n89 FROM length_year_matrix_" + arguments.ll + " WHERE year = ", i, "lengths", arguments.ll))
      else:
        tasks.put(Task("SELECT e180 FROM length_year_matrix_" + arguments.ll + " WHERE year = ", i, "lengths", arguments.ll))

  for i in range(num_processors):
    tasks.put(None)