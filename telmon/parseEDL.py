import re
import io
from time import gmtime, strftime, time

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
	#edlData = EDLData()
	
    with open(filepath, 'r') as file:
        line = next(file)
        while line:
            parsedLine = _EdlLine(line)
            #edlData.append(parsedLine)
        line = next(file,None)
	
    return edlData
    
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
            if re.search('\d{4}\-\d{1,2}\-\d{1,2}\s\d{2}\:\d{2}\:\d{2}',filedate):
                self.filedtg = filedate
            else:
                err = 'Date format should be 2017-3-2017 19:00:00 NOT: ' + filedate
                raise ValueError(err) 
        else:
            self.filedtg = strftime("%Y-%m-%d %H:%M:%S", gmtime())     
            
    def parseline(self, line):
	# check on what kind of a line has been received, then parse it
        if(line == None):
            raise RuntimeError('Null Value') 
        if re.search('SOURCE*',line):
            a = line.split(' ');
            source = a[1]
            self.SOURCE = source
            return 
        if re.search('STATION*',line):
            a = line.split(' ');
            station = a[1]
            self.STATION = station
            return 
        if re.search('DEVICE*',line):
            a = line.split(' ');
            device = a[1]
            self.DEVICE = device
            return 
        if re.search('OVERWRITE*',line):
            a = line.split(' ');
            overwrite = a[1]
            self.OVERWRITE = overwrite
            return 
        if re.search('\d{4}\/\d{1,2}\/\d{1,2}',line):
            #Taking advantage of standard format, not very spart parsing.
            tempdate = line[1:17]
            monitordate = tempdate.replace('/','-')
            data = line[20:]
            self.timeanddatum.append( [monitordate, data])
            return 
            
        err = 'Do not recognize: ' + line
        raise ValueError(err)           

 
 