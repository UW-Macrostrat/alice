import multiprocessing
import argparse
from multiprocessor import *

parser = argparse.ArgumentParser(
  description="Populate the result matrices of Alice",
  epilog="Example usage: python collect.py -t gaps")

parser.add_argument("-t", "--type", dest="type",
  default="lengths", type=str, required=True,
  help="Type of data to collect. Can be either 'lengths' or 'gaps'.")

arguments = parser.parse_args()

if __name__ == '__main__':
  tasks = multiprocessing.JoinableQueue()
  results = multiprocessing.Queue()

  num_processors = multiprocessing.cpu_count() - 2
  processors = [Processor(tasks, results) for i in xrange(num_processors)]

  for each in processors:
    each.start()
  
  # Set the range to whatever year you want to go up to (551 is the max)
  for i in xrange(551):
    if arguments.type == "gaps":
      tasks.put(Task("SELECT n89 FROM gaps250 WHERE year = ", i, "gaps"))
    else:
      tasks.put(Task("SELECT n89 FROM length_year_matrix WHERE year = ", i, "lengths"))

  for i in range(num_processors):
    tasks.put(None)