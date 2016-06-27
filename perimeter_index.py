import psycopg2
from psycopg2.extensions import AsIs
import csv

try:
  conn = psycopg2.connect(dbname="alice", user="john", host="localhost", port=5439)
except:
  print "Could not connect to database: ", sys.exc_info()[1]
  sys.exit()

cursor = conn.cursor()

results = []

for year in xrange(0, 551):
    print year
    cursor.execute("""
        WITH perim AS (
            SELECT 2 * pi() * (sqrt(sum(ST_Area(geom::geography)/1000000)) / pi()) zero
            FROM chunks_can.reconstructed_%(year)s
        ),
        c AS (
            SELECT sum(ST_Perimeter(geom::geography) * 0.001) s FROM chunks_can.reconstructed_%(year)s
        ),
        m AS (
            SELECT sum(ST_Perimeter(geom::geography) * 0.001) s FROM merge.reconstructed_%(year)s_merged
            WHERE plateid IN (select distinct plateid FROM merge.reconstructed_550_merged)
        )
        SELECT (c.s - (select zero FROM perim)) / (m.s - (select zero FROM perim)) FROM c, m

    """, {
        "year": AsIs(year)
    })
    result = cursor.fetchone()
    results.append({
        "year": year,
        "avg_distance": result[0]
    })


with open('perimeter_output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['year', 'avg_distance'])
    writer.writerow({'year': 'year', 'avg_distance': 'avg_distance'})
    for row in results:
        writer.writerow(row)
