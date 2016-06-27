import psycopg2

conn = psycopg2.connect(dbname="alice", user="john", host="localhost", port=5432)
cur = conn.cursor()

cur.execute("""
    DROP TABLE IF EXISTS laurentia_p_index;

    CREATE TABLE laurentia_p_index (
        year integer,
        l_length numeric,
        l_sublength numeric
    );
""")
conn.commit()

for year in xrange(0, 551):
    cur.execute("""
        INSERT INTO laurentia_p_index (year, l_length, l_sublength)
        WITH notLaurentia AS (
          SELECT ST_Union(geom) geom
          FROM merge.reconstructed_""" + str(year) + """_merged
          WHERE plateid != 101 AND plateid IN (
            SELECT DISTINCT plateid
            FROM merge.reconstructed_550_merged
            WHERE plateid != 101
          )
        ),
        laurentia AS (
          SELECT ST_Union(geom) geom
          FROM (
            SELECT ST_ExteriorRing((ST_Dump(geom)).geom) geom
            FROM merge.reconstructed_""" + str(year) + """_merged
            WHERE plateid = 101
          ) sub
        )
        SELECT """ + str(year) + """ AS year, ST_Length(l.geom::geography) AS l_length, ST_Length(ST_Difference(l.geom, nl.geom)::geography) l_sublength
        FROM laurentia l, notLaurentia nl
    """)
    print year

conn.commit()
