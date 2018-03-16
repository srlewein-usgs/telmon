import unittest
import io

from telmon.parseEDL import _EdlLine, parseStream

class TestExpMatch(unittest.TestCase):

    def setup(self):
        self.test_sourceline = '//SOURCE nwiswa EDL'
        self.test_stationline = '//STATION 12113390'
        self.test_deviceline = '//DEVICE GRFILTF-1'
        self.test_overwriteline = '//OVERWRITE true'
        self.test_dataline = '"2018/02/19 02:00", 3188.3097222222264'
        self.test_bogusline = 'blahblah blah'
    
    def test_sourceline(self):

        edlregex = _EdlLine('//SOURCE nwiswa EDL')
        self.assertEqual(edlregex.retVal[0],'SOURCE')
        self.assertEqual(edlregex.retVal[1], 'nwiswa')
        
    def test_stationline(self):

        edlregex = _EdlLine('//STATION 12113390')
        self.assertEqual(edlregex.retVal[0],'STATION')
        self.assertEqual(edlregex.retVal[1], '12113390')
        
    def test_deviceline(self):

        edlregex = _EdlLine('//DEVICE GRFILTF-1')
        self.assertEqual(edlregex.retVal[0],'DEVICE')
        self.assertEqual(edlregex.retVal[1], 'GRFILTF-1')
        
    def test_overwriteline(self):

        edlregex = _EdlLine('//OVERWRITE true')
        self.assertEqual(edlregex.retVal[0],'OVERWRITE')
        self.assertEqual(edlregex.retVal[1], 'true')
        
    def test_dataline(self):

        edlregex = _EdlLine('"2018/02/19 02:00", 3188.3097222222264')
        self.assertEqual(edlregex.retVal[0],'DATA')
        self.assertEqual(edlregex.retVal[1], '2018/02/19') 
        self.assertEqual(edlregex.retVal[2], '02:00') 
        self.assertEqual(edlregex.retVal[3], '3188.3097222222264') 
        
    def test_bogusline(self):

        with self.assertRaises(ValueError):  
            edlregex = _EdlLine('blahblah blah')       
    
    def test_blankline(self):
         with self.assertRaises(ValueError):  
            edlregex = _EdlLine('')    

    def test_nothing(self):
         with self.assertRaises(RuntimeError):  
            edlregex = _EdlLine(None)              

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
        
            
if __name__ == '__main__':
    unittest.main()