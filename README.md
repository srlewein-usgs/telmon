# telmon
The purpose of this project is to perform some experiments to test the efficacy
of building some telemetry monitoring tools on top of the time-series application suite.

Workflow Overview

A file is acquired - GOES or Rsync - on the telemetry server file system.

The file write is an event that triggers a process that will read the file 
and file system information. Information to be retrieved initially includes
     - System time that the file was received
	 - File name
	 - Source
	 - Station Name
	 - Array of time entries
	 
The hope is that AWS lambda integration will be used to capture and process the file read event.

Once the event data is captured, write the information to a data store - probably red-shift.

Create an API to access the information. Samples might include:
     - Return all stations with file updates between early time and last time
	 - Return all stations with gaps in time entries between timeA and timeB
	 - Retrun all stations that have not been updated between timeA and timeB
	 - Return update times for an array of stations
	 - Returne time entries for an array of stations.
	 
Integrate with location services to display a map where telemetry information may be viewed.
