#Alice

## Dependencies
- Python 2.7+
- [PostgreSQL](http://www.postgresql.org) 9.1+ and [PostGIS](http://postgis.net) 2.0+
- [psycopg2](http://initd.org/psycopg/) ([OS X installation](https://gist.github.com/jczaplew/26e123fb64cf448cd065))
- MySQLdb (*Optional for step 8* ) - refer [here](https://gist.github.com/jczaplew/4bf9adc21305bc4efee1) for installation instructions on Mavericks



## Setup
**Note:**  the scripts ````collect.py```` and ````get_jaccard.py```` use the Python module [Multiprocessing](https://docs.python.org/2/library/multiprocessing.html), which leverages all available CPUs for a faster processing time. The config param ````cpus_free```` has a default value of 2, meaning 2 CPUs will remain free for any other tasks on the same machine. If you desire more or less to remain free, please change the default value in ````config.py````.

***^*** indicates that this step takes a considerable amount of time to complete

1. Edit ````config.py.example```` with your Postgres username, port, and host, as well as MySQL credentials, if applicable (only needed for Step 8). Rename to or save as ````config.py````.

2. Run ````python go_ask.py````. This will create a Postgres database ````alice```` and populate it with all the tables necessary for the analysis. It will take a while to run.

3. Run ````python areas.py```` to populate the table ````areas```` and the column ````area```` of the table````name_lookup````.  

4. Run ````python centroids.py```` to populate the table ````centroid_matrix````.

5.  ***^*** Run ````python azimuth.py````. This populates the first half of table ````distance_azimuth_matrix````, including the fields ````platea````, ````plateb````, ````shortest_line````,  ````distance````, and ````direction````.

6. ***^*** Run ````python chunks.py````. This populates the schema ````chunks```` and the table ````chunk_matrix````.

7.  ***^*** Run ````python chunks_can.py````. This populates the schema ````chunks_can```` and the table ````chunk_matrix_can````.

8. ***^***  Run ````python collect.py -t lengths -l lat````. This populates the table ````length_year_matrix_lat````, and creates multiple processes in an attempt to fill the table as quickly as possible. 

9. ***^***  Run ````python collect.py -t lengths -l lng````. This populates the table ````length_year_matrix_lng````, and creates multiple processes in an attempt to fill the table as quickly as possible. 

10.  ***^*** Run ````python collect.py -t gaps -l lat````. This populates the tables ````gaps250_lat````, ````gaps500_lat````, ````gaps1000_lat````, and ````gaps1500_lat````. 

11.  ***^*** Run ````python collect.py -t gaps -l lng```` to populate the tables ````gaps250_lng````, ````gaps500_lng````, ````gaps1000_lng````, and ````gaps1500_lng````.

12.  ***^*** Run ````python collect.py -t lengths_can -l lat```` to populate the table ````length_year_matrix_can_lat````.

13.  ***^*** Run ````python collect.py -t lengths_can -l lng```` to populate the table ````length_year_matrix_can_lng````.

14. ***^*** Run ````python collect.py -t gaps_can -l lat```` to populate the tables ````gaps250_can_lat````, ````gaps500_can_lat````, ````gaps1000_can_lat````, and ````gaps1500_can_lat````.

15.  ***^*** Run ````python collect.py -t gaps_can -l lng```` to populate the tables ````gaps250_can_lng````, ````gaps500_can_lng````, ````gaps1000_can_lng````, and ````gaps1500_can_lng````.

16.  ***^*** (**Optional **- requires a local dump of the [Paleobiology Database](http://paleobiodb.org)) - Run ````python get_genera.py````, which populates the table ````plate_genera````, followed by ````python get_jaccard.py````. This populates the second half of table ````distance_azimuth_matrix````, including the fields ````uunion````, and ````intersection````, which can used to compute a [Jaccard Index](http://en.wikipedia.org/wiki/Jaccard_index).

## Schemas

| Schema        | Description           | Populated by  |
| ------------- | --------------------------- | ------------ |
| chunks             |  Geometry dissolved on touching (ex: if three polygons touch and surrounded by "water", they are one polygon in this dataset)    | *chunks.py* |
| chunks_can     |  Same as ````chunks```` but uses only plates with an age > 500MA    | *chunks_can.py* |
| merge      |  Same as ````orig````, but ST_Union(geom) GROUP BY plateid    | *populated at start* |
| orig          |  Contains cleaned, but original, data from GPlates    | *populated at start* |
| public       |  Holds result matrices  | *populated at start* |

## Tables

| Tables        | Description              | Populated by  |
| ------------- | --------------------------- | ------------ |
| areas                                           | The area of each plate in km<sup>2</sup> in each year  | ````areas.py```` |  
| centroid_matrix                            | Distance from the centroid of all plates in all years to the equator and prime meridian (in degrees)   | ````centroids.py```` |  
| chunk_matrix                              | Plate lookup for chunked geometry  | ````chunks.py```` |  
| chunk_matrix_can                      | Plate lookup for canonical chunked geometry  | ````chunks_can.py```` |  
| chunk_summary                         | Numbers of chunks in each year  | ````chunks.py```` |  
| distance_azimuth_matrix            | Indicates shortest line, length of shortest line, and azimuth of shortest line between all plate pairs across all years; also includes intersection and union of genus occurrences for plate pair |  ````python azimuth.py```` & ````python get_jaccard.py````  |
| gaps*x*_lat                                  | Number of gaps > *x* km between plates at each line of latitude   |    ````collect.py -t gaps -l lat````  | 
| gaps*x*_lng                                  | Number of gaps > *x* km between plates at each line of longitude   |    ````collect.py -t gaps -l lng````  | 
| gaps*x*_can_lat                           | Number of gaps > *x* km between plates at each line of latitude using canonical plates  |    ````collect.py -t gaps_can -l lat````  | 
| gaps*x*_can_lng                         | Number of gaps > *x* km between plates at each line of longitude  using canonical plates |    ````collect.py -t gaps_can -l lng````  | 
| length_year_matrix_lat 		    | Amount of land (in km) at each line of latitude over time      |    ````collect.py -t lengths -l lat````  |
| length_year_matrix_lng  	           | Amount of land (in km) at each line of longitude over time      |    ````collect.py -t lengths -l lng````  |
| length_year_matrix_can_lat        | Amount of land (in km) at each line of latitude over time using canonical plates      |    ````collect.py -t lengths_can -l lat````  |
| length_year_matrix_can_lng  	    | Amount of land (in km) at each line of longitude over time using canonical plates      |    ````collect.py -t lengths_can -l lng````  |
| name_lookup  				    | Lookup plate names by id     |    *populated at start*  |
| ne_50m_graticules_1                  | 1 degree graticule from [Natural Earth Data](http://www.naturalearthdata.com/downloads/50m-physical-vectors/50m-graticules/)                 | *populated at start* |
| plate_genera                               | Number of unique genera on a given plate at a given point in time   | ````get_genera.py```` |  


## License
All code unique to Alice carries a [CC0](http://creativecommons.org/about/cc0) license. All paleogeographic data was originally derived from [GPlates](http://www.gplates.org/) using a [GNU General Public License, V2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html) license, and was [modified heavily throughout 2014](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html#SEC3) for the purposes of this research.

