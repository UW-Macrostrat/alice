#Alice

## Setup
1. Edit ````setup.sh```` with your desired Postgres username, port, and host

2. Run ````./setup.sh````. This will create a Postgres database ````alice```` and populate it with all the tables necessary for the analysis. It will take a while to run.

3. Run ````python collect.py -t lengths -l lat````. This populates the table ````length_year_matrix_lat````, and creates multiple processes in an attempt to fill the table as quickly as possible. If you prefer to populate the table with a single process, you can use ````get_lengths.py````.

4. Run ````python collect.py -t gaps -l lat````. This populates the tables ````gaps250_lat````, ````gaps500_lat````, ````gaps1000_lat````, and ````gaps1500_lat````. Again, this creates multiple processes, and you can use ````get_gaps.py```` instead if you want to use a single process.

5. Run ````python azimuth.py -l lat````. This populates the table ````distance_azimuth_matrix_lat````.