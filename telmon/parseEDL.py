from re import search
from os.path import getmtime, basename 
from json import dumps
from time import gmtime, strftime, time
import sys, getopt

def parseFile(filepath):
    """
	Parse an EDL file at a given filepath
	
	Parameters
	----------
	filepath : str
	    Filepath for the file to be parsed
	
	Returns
	---------
	data : EDL file serialized as JSON objects
	
	"""

    file = open(filepath, 'r')
    fname = basename(filepath)
    dtg = strftime("%Y-%m-%d %H:%M:%S",gmtime(getmtime(filepath)))  
    edlFile = EdlFile(fname, dtg)    
    line = next(file)
    while line:
        edlFile.parseline(line.rstrip())
        line = next(file,None)
    file.close()
    return edlFile.serialize()
    
def parseStream(input):
#     """
#         Parse an EDL stream
#         
#        Parameters
#         ----------
#         stream: StringIO
#         
#         Returns
#         ----------
#         data: EDL file serialized as JSON object
#        """

    input.seek(0)
    print(input.getvalue())
    parsedLines = []
    line = input.readline();
    while line:
        parsedLine = _EdlLine(line)
        parsedLines.append(parsedLine.retVal)
        line = input.readline()
        print('loop')
    input.close()
    return parsedLines
    
	
class EdlFile:
    """
        Parse a line using regex to determine line type
        Throws RuntimeException if passed a null value
        Throws ValueException if line is not recognized
        
        Values are returned as simple lists, caller will need to know 
        what to do with lists.
        
        JSON structure of an EDL file
        {
            "filename": "afile name",
            "filedtg": "2017-3-2017 19:00:00",
            "SOURCE": "nwisa",
            "STATION": "12113390",
            "DEVICE": "GRFILTF-1",
            "OVERWRITE": "true",
            "timeanddatum": [ 
                ["2018-02-19 02:00", "3188.3097222222264"],
                ["2018-02-19 03:00", "3188.3097222222264"]
                ]
        }
            
    """
   
   
    filename = None
    filedtg = None
    SOURCE = None
    STATION = None
    DEVICE = None
    OVERWRITE = None
    timeanddatum = []

    def __init__(self, fileName, filedate):
        #If No name is assigned, make one up
        if fileName:
             self.filename = fileName
        else:
             suffix = str(int(round(time())))
             self.filename = 'assigned' + suffix
        if filedate:
            if search('\d{4}\-\d{1,2}\-\d{1,2}\s\d{2}\:\d{2}\:\d{2}',filedate):
                self.filedtg = filedate
            else:
                err = 'Date format should be 2017-3-2017 19:00:00 NOT: ' + filedate
                raise ValueError(err) 
        else:
            self.filedtg = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        #initialize rest of the class variables
        self.SOURCE = None
        self.STATION = None
        self.DEVICE = None
        self.OVERWRITE = None
        self.timeanddatum = []
            
    def parseline(self, line):
	# check on what kind of a line has been received, then parse it
        if(line == None):
            raise RuntimeError('Null Value') 
        if search('SOURCE*',line):
            a = line.split(' ');
            source = a[1]
            self.SOURCE = source
            return 
        if search('STATION*',line):
            a = line.split(' ');
            station = a[1]
            self.STATION = station
            return 
        if search('DEVICE*',line):
            a = line.split(' ');
            device = a[1]
            self.DEVICE = device
            return 
        if search('OVERWRITE*',line):
            a = line.split(' ');
            overwrite = a[1]
            self.OVERWRITE = overwrite
            return 
        if search('\d{4}\/\d{1,2}\/\d{1,2}',line):
            #Taking advantage of standard format, not very spart parsing.
            tempdate = line[1:17]
            monitordate = tempdate.replace('/','-')
            data = line[20:]
            self.timeanddatum.append( [monitordate, data])
            return 
            
        err = 'Do not recognize: ' + line
        raise ValueError(err)           

    def serialize(self):
     
        #if there are not values for every output, throw a RuntimeError
        self.isincomplete()
        serializedJson = dumps({'filename':self.filename, 'filedtg':self.filedtg,'SOURCE':self.SOURCE,
        'STATION':self.STATION,'DEVICE':self.DEVICE,'OVERWRITE':self.OVERWRITE,'timeanddatum':self.timeanddatum})
        return serializedJson
     
     
    def isincomplete(self):
     
        error = []
        
        if self.filename == None:
            error.append('filename')
        elif self.filedtg == None:
            error.append('filedtg')
        elif self.SOURCE == None:
            error.append('SOURCE')
        elif self.STATION == None:
            error.append('STATION')
        elif self.DEVICE == None:
            error.append('DEVICE')
        elif self.OVERWRITE == None:
            error.append('OVERWRITE')
        elif self.timeanddatum == []:
            error.append('timeanddatum')
        
        if error == []:
            return False
        
        errmsg = 'Missing data for: ' + str(error)
        raise RuntimeError(errmsg)    

def main2(argv):
    filetoparse = ''
    databaseconnectstr = '' 
    user = ''
    pwd = ''
    try:
        opts, args = getopt.getopt(argv,'hf:c:u:p:')
    except getopt.GetoptError:
        print ('parseEDL.py -f <file> -c <dbconnect> -u <user> -p <password>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print ('parseEDL.py -f <file> -c <dbconnect> -u <user> -p <password>')
            sys.exit()
        elif opt == '-f':
            filetoparse = arg
        elif opt == '-c':
            databaseconnectstr = arg
        elif opt == '-u':
            user = arg
        elif opt == '-p':
            pwd = arg
    if filetoparse == '':
        print('parseEDL.py -f file')
       
    print ('Load file ' + filetoparse + ' to ' + databaseconnectstr + ' user: ' + user + ' pwd: xxxxx')                   
    jsonobj = parseFile(filetoparse)
    print(jsonobj)
    print ('Completed ' + filetoparse)
         
  
if __name__== "__main__":
    main2(sys.argv[1:])
 