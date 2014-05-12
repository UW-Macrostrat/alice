#Alice

## Setup
1. Edit ````config.py```` with your Postgres username, port, and host

2. Run ````python setup.py````. This will create a Postgres database ````alice```` and populate it with all the tables necessary for the analysis. It will take a while to run.

3. Run ````python collect.py -t lengths -l lat````. This populates the table ````length_year_matrix_lat````, and creates multiple processes in an attempt to fill the table as quickly as possible. If you prefer to populate the table with a single process, you can use ````get_lengths.py````.
4. Run ````python collect.py -t lengths -l lng```` to populate the table ````length_year_matrix_lng````. 

5. Run ````python collect.py -t gaps -l lat````. This populates the tables ````gaps250_lat````, ````gaps500_lat````, ````gaps1000_lat````, and ````gaps1500_lat````. Again, this creates multiple processes, and you can use ````get_gaps.py```` instead if you want to use a single process.
6. Run ````python collect -t gaps -l lng```` to populate the tables ````gaps250_lng````, ````gaps500_lng````, ````gaps1000_lng````, and ````gaps1500_lng````.

5. Run ````python azimuth.py -l lat````. This populates the table ````distance_azimuth_matrix_lat````.


| Tables        | Description              | Populate  |
| ------------- |:---------------------------:| ------------:|
| distance_azimuth_matrix            | Indicates shortest line, length of shortest line, and azimuth of shortest line between all plate pairs across all years |  ````azimuth.py -l lat````  |
| gaps250_lat                                 | Number of gaps > 250km between plates at each line of latitude     |    ````collect.py -t gaps -l lat````  | 
| gaps250_lng 				    | Number of gaps > 250km between plates at each line of longitude        |    ````collect.py -t gaps -l lng````  |
| gaps500_lat  				    | Number of gaps > 500km between plates at each line of latitude    |    ````collect.py -t gaps -l lat````  |
| gaps500_lng  				    | Number of gaps > 500km between plates at each line of longitude      |    ````collect.py -t gaps -l lng````  |
| gaps1000_lat  				    | Number of gaps > 1000km between plates at each line of latitude         |    ````collect.py -t gaps -l lat````  |
| gaps1000_lng  				    | Number of gaps > 1000km between plates at each line of longitude     |    ````collect.py -t gaps -l lng````  | 
| gaps1500_lat  			           | Number of gaps > 1500km between plates at each line of latitude         |    ````collect.py -t gaps -l lat````  |
| gaps1500_lng  				    | Number of gaps > 1500km between plates at each line of longitude      |    ````collect.py -t gaps -l lng````  |
| length_year_matrix_lat 		    | Amount of land at each line of latitude over time      |    ````collect.py -t lengths -l lat````  |
| length_year_matrix_lng  	           | Amount of land at each line of longitude over time      |    ````collect.py -t lengths -l lng````  |
| name_lookup  				    | Lookup plate names by id     |    *populated at start*  |
