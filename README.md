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


Tests can be run by `python3 -m unittest` from the project directory.

================================================
Preparing centos 6 system to run telmon

Intstall inotifywait 
  yum --enablerepo=epel -y install inotify-tools

Install Python 3.6
# Compilers and related tools:
yum groupinstall -y "development tools"

# Libraries needed during compilation to enable all features of Python:
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel expat-devel

# If you are on a clean "minimal" install of CentOS you also need the wget tool:
yum install -y wget


# Python 3.6.3:
wget http://python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
tar xf Python-3.6.3.tar.xz
cd Python-3.6.3
./configure --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
sudo make  
sudo make altinstall

wget https://bootstrap.pypa.io/get-pip.py
python3.6 get-pip.py

this will result in a local install that is callable by python3.6

