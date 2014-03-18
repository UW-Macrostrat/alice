#Alice

## Setup
1. Edit ````config.py```` with your desired Postgres username, port, and host
2. Run ````python setup_db.py````. This will create a Postgres database ````alice```` and populate it with all the tables necessary for the analysis. It will take a while to run.
3. Run ````python get_lengths_multiprocess.py````. This populates the table ````length_year_matrix````. This will create multiple processes in an attempt to fill the table as quickly as possible. If you prefer to populate the table with a single process, you can use ````get_lengths.py````.
4. Run ````python get_gaps_multiprocess.py````. This populates the tables ````gaps250````, ````gaps500````, ````gaps1000````, and ````gaps1500````. Again, this creates multiple processes, and you can use ````get_gaps.py```` instead if you want to use a single process.