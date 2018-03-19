import unittest
import io
import os
import json

from ..parseEDL import EdlFile, parseStream, parseFile

class TestExpMatch(unittest.TestCase):

    def test_initializeparseobject(self):
         edl = EdlFile('Afile', '2017-12-12 10:00:00')
         self.assertEqual(edl.filename, 'Afile')
         self.assertEqual(edl.filedtg, '2017-12-12 10:00:00')
    
    def test_nofilename(self):
        edl = EdlFile('', '2017-12-12 10:00:00')
        self.assertTrue(edl.filename.startswith('assigned'))
    
    def test_baddateformat(self):
        with self.assertRaises(ValueError):  
            edl = EdlFile('Afile','2017/12/12 10:00:00')
            
    def test_nodate(self):
        edl = EdlFile('Afile', '')
        self.assertIsNotNone(edl.filedtg)
    
    def test_sourceline(self):

        edlFile = EdlFile('Afile', '2017-12-12 10:00:00')
        edlFile.parseline('//SOURCE nwiswa EDL')
        self.assertEqual(edlFile.SOURCE,'nwiswa')
        
    def test_stationline(self):

        edlFile = EdlFile('Afile', '2017-12-12 10:00:00')
        edlFile.parseline('//STATION 12113390')
        self.assertEqual(edlFile.STATION,'12113390')
       
    def test_deviceline(self):

        edlFile = EdlFile('Afile', '2017-12-12 10:00:00')
        edlFile.parseline('//DEVICE GRFILTF-1')
        self.assertEqual(edlFile.DEVICE,'GRFILTF-1')
       
    def test_overwriteline(self):

        edlFile = EdlFile('Afile', '2017-12-12 10:00:00')
        edlFile.parseline('//OVERWRITE true')
        self.assertEqual(edlFile.OVERWRITE,'true')
         
    def test_dataline(self):

        edlFile = EdlFile('Afile', '2017-12-12 10:00:00')
        edlFile.parseline('"2018/02/19 02:00", 3188.3097222222265')
        self.assertEqual(edlFile.timeanddatum[0][0],'2018-02-19 02:00')
        self.assertEqual(edlFile.timeanddatum[0][1], '3188.3097222222265') 

    def test_bogusline(self):
 
        with self.assertRaises(ValueError):  
            edlFile = EdlFile('Afile', '2017-12-12 10:00:00')
            edlFile.parseline('blahblah blah')       
  
    def test_blankline(self):
    
         with self.assertRaises(ValueError): 
            edlFile = EdlFile('Afile', '2017-12-12 10:00:00')         
            edlFile.parseline('blahblah blah')     

    def test_nothing(self):
    
         with self.assertRaises(RuntimeError): 
            edlFile = EdlFile('Afile', '2017-12-12 10:00:00')         
            edlFile.parseline(None)   
            
class TestSerialization(unittest.TestCase):
   
    def test_jsonoutput(self):
        
        edlFile = EdlFile('Afile', '2017-12-12 10:00:00')
        edlFile.parseline('//SOURCE nwiswa EDL')
        edlFile.parseline('//STATION 12113390')
        edlFile.parseline('//DEVICE GRFILTF-1')
        edlFile.parseline('//OVERWRITE true')
        edlFile.parseline('"2018/02/19 02:00", 3188.3097222222264')
        ret_json = edlFile.serialize()
        parsed_json = json.loads(ret_json)
        self.assertEqual('Afile', parsed_json['filename'])
        self.assertEqual('2017-12-12 10:00:00', parsed_json['filedtg'])
        self.assertEqual('nwiswa', parsed_json['SOURCE'])
        self.assertEqual('12113390', parsed_json['STATION'])
        self.assertEqual('GRFILTF-1', parsed_json['DEVICE'])
        self.assertEqual('true', parsed_json['OVERWRITE'])
        self.assertEqual('2018-02-19 02:00', parsed_json['timeanddatum'][0][0])
        self.assertEqual('3188.3097222222264', parsed_json['timeanddatum'][0][1])
       
    def test_incomplete(self):
    
        with self.assertRaises(RuntimeError): 
            edlFile = EdlFile('Afile', '2017-12-12 10:00:00') 
            ret_json = edlFile.serialize()
        
class TestFileInput(unittest.TestCase):

    def test_loadfile(self):
    
        fileandpath = os.path.abspath('telmon/test/testedl.txt')
        ret_json = parseFile(fileandpath)
        parsed_json = json.loads(ret_json)
        self.assertIsNotNone(ret_json)
        # just spot check
        self.assertEqual('12113390', parsed_json['STATION'])
        
        
        
"""
class TestStreamInput(unittest.TestCase):  

    def test_goodstream(self):
        input = io.StringIO()
        input.write('//SOURCE nwiswa EDL\n')
        input.write('//STATION 12113390\n')
        input.write('//DEVICE GRFILTF-1\n')
        input.write('//OVERWRITE true\n')
        input.write('"2018/02/19 02:00", 3188.3097222222264\n')
        retVal = parseStream(input)
        print(retVal)
"""        
            
if __name__ == '__main__':
    unittest.main()