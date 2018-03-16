import re
import io

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
    
	
class _EdlLine:
    """
        Parse a line using regex to determine line type
        Throws RuntimeException if passed a null value
        Throws ValueException if line is not recognized
        
        Values are returned as simple lists, caller will need to know 
        what to do with lists.
    """
	

    retVal = None
	
    def __init__(self, line):
	# check on what kind of a line has been received, then parse it
        if(line == None):
            raise RuntimeError('Null Value') 
        if re.search('SOURCE*',line):
            a = line.split(' ');
            source = a[1]
            self.retVal = ['SOURCE', source]
            return 
        if re.search('STATION*',line):
            a = line.split(' ');
            station = a[1]
            self.retVal = ['STATION', station]
            return 
        if re.search('DEVICE*',line):
            a = line.split(' ');
            device = a[1]
            self.retVal = ['DEVICE', device]
            return 
        if re.search('OVERWRITE*',line):
            a = line.split(' ');
            overwrite = a[1]
            self.retVal = ['OVERWRITE', overwrite]
            return 
        if re.search('\d{4}\/\d{1,2}\/\d{1,2}',line):
            a = line.split(' ');
            mondate1 = a[0]
            mondate = mondate1[1:]
            timehack1 = a[1]
            timehack = timehack1[:-2]
            data = a[2]
            self.retVal = ['DATA', mondate, timehack, data]
            return 
            
        err = 'Do not recognize: ' + line
        raise ValueError(err)           

 
 