DROP TABLE telemetry_files;

CREATE TABLE telemetry_files {
    source  text,
	station text,
	file_name text,
	file_dtg timestamp
};

DROP TABLE telemetry_measures;

CREATE TABLE telemetry_measures {
     source text,
	 station text,
	 device text,
	 overwrite text,
	 measurement_time timestamp,
	 measurement_data text,
	 
};

