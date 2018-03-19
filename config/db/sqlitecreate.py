import sqlite3

sqlite_file = 'telmon_test_db'

# connect to the db file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Create File table
c.execute('CREATE TABLE telemetry_files(source text, station text, file_name text, file_dtg text)')

c.execute('CREATE TABLE telemetry_measures(source text, device text,\
            overwrite text, measurement_time text, measurement_data text)')

conn.commit()
conn.close()