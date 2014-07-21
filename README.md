#Alice

## Dependencies
- Python 2.7+
- PostgreSQL 9.1+ and PostGIS 2.0+
- psycopg2 - ````sudo port install py27-psycopg2````
- MySQLdb (*Optional for step 8* ) - refer [here](https://gist.github.com/jczaplew/4bf9adc21305bc4efee1) for installation instructions on Mavericks



## Setup
**Note: **  the scripts ````collect.py```` and ````get_jaccard.py```` use the Python module [Multiprocessing](https://docs.python.org/2/library/multiprocessing.html), which leverages all available CPUs for a faster processing time. The config param ````cpus_free```` has a default value of 2, meaning 2 CPUs will remain free for any other tasks on the same machine. If you desire more or less to remain free, please change the default value in ````config.py````.

***^*** indicates that this step takes a considerable amount of time to complete

1. Edit ````config.py.example```` with your Postgres username, port, and host, as well as MySQL credentials, if applicable (only needed for Step 8). Rename to or save as ````config.py````.

2. Run ````python go_ask.py````. This will create a Postgres database ````alice```` and populate it with all the tables necessary for the analysis. It will take a while to run.

3. Run ````python areas.py```` to populate the table ````areas```` and the column ````area```` of the table````name_lookup````.  

4. Run ````python centroids.py```` to populate the table ````centroid_matrix````.

5.  ***^*** Run ````python azimuth.py````. This populates the first half of table ````distance_azimuth_matrix````, including the fields ````platea````, ````plateb````, ````shortest_line````,  ````distance````, and ````direction````.

6. ***^*** Run ````python chunks.py````. This populates the schema ````chunks```` and the table ````chunk_matrix````.

7. ***^***  Run ````python collect.py -t lengths -l lat````. This populates the table ````length_year_matrix_lat````, and creates multiple processes in an attempt to fill the table as quickly as possible. 

8. ***^***  Run ````python collect.py -t lengths -l lng````. This populates the table ````length_year_matrix_lng````, and creates multiple processes in an attempt to fill the table as quickly as possible. 

9.  ***^*** Run ````python collect.py -t gaps -l lat````. This populates the tables ````gaps250_lat````, ````gaps500_lat````, ````gaps1000_lat````, and ````gaps1500_lat````. 

10.  ***^*** Run ````python collect.py -t gaps -l lng```` to populate the tables ````gaps250_lng````, ````gaps500_lng````, ````gaps1000_lng````, and ````gaps1500_lng````.

11.  ***^*** (**Optional **- requires a local dump of the [Paleobiology Database](http://paleobiodb.org)) - Run ````python get_genera.py````, which populates the table ````plate_genera````, followed by ````python get_jaccard.py````. This populates the second half of table ````distance_azimuth_matrix````, including the fields ````uunion````, and ````intersection````, which can used to compute a [Jaccard Index](http://en.wikipedia.org/wiki/Jaccard_index).

## Schemas

| Schema        | Description           | Populate  |
| ------------- | --------------------------- | ------------ |
| chunks     |  Geometry dissolved on touching (ex: if three polygons touch and surrounded by "water", they are one polygon in this dataset)    | *chunks.py* |
| merge      |  Same as ````orig````, but ST_Union(geom) GROUP BY plateid    | *populated at start* |
| orig          |  Contains cleaned, but original, data from GPlates    | *populated at start* |
| public       |  Holds result matrices  | *populated at start* |

## Tables

| Tables        | Description              | Populate  |
| ------------- | --------------------------- | ------------ |
| areas                                           | The area of each plate in km<sup>2</sup> in each year  | ````areas.py```` |  
| centroid_matrix                            | Distance from the centroid of all plates in all years to the equator and prime meridian (in degrees)   | ````centroids.py```` |  
| chunk_matrix                              | Plate lookup for chunked geometry  | ````chunks.py```` |  
| distance_azimuth_matrix            | Indicates shortest line, length of shortest line, and azimuth of shortest line between all plate pairs across all years |  ````python azimuth.py```` & ````python get_jaccard.py````  |
| gaps*x*_lat                                  | Number of gaps > *x* km between plates at each line of latitude   |    ````collect.py -t gaps -l lat````  | 
| gaps*x*_lng                                  | Number of gaps > *x* km between plates at each line of longitude   |    ````collect.py -t gaps -l lng````  | 
| length_year_matrix_lat 		    | Amount of land at each line of latitude over time      |    ````collect.py -t lengths -l lat````  |
| length_year_matrix_lng  	           | Amount of land at each line of longitude over time      |    ````collect.py -t lengths -l lng````  |
| name_lookup  				    | Lookup plate names by id     |    *populated at start*  |
| ne_50m_graticules_1                  | 1 degree graticule from [Natural Earth Data](http://www.naturalearthdata.com/downloads/50m-physical-vectors/50m-graticules/)                 | *populated at start* |
| plate_genera                               | Number of unique genera on a given plate at a given point in time   | ````get_genera.py```` |  
| reconstructed_x_merged            |  Contains the reconstucted geometry for each year     | *populated at start* |


