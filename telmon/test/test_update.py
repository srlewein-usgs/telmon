import unittest
import sqlite3

from ..uploadEDL import UploadEdl

class TestUpload(unittest.TestCase):
    
    conn = None
    smalljson = None
    
    def setUp(self):
        
        # Connect to test db
        sqlite_file = 'telmon/test/telmon_test_db'
        self.conn = sqlite3.connect(sqlite_file)
        
        #load small json object
        file = open('telmon/test/small.json', 'r')
        self.smalljson = file.read()
        file.close()
 
    def test_loaddb(self):
        
        uploader = UploadEdl(self.conn, self.smalljson)
        self.conn.commit()
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM telemetry_files')
        retval = c.fetchall()
        print(retval)
        val1 = retval[0][0]
        self.assertEqual(1, val1)

       
    def tearDown(self):

        c = self.conn.cursor()
        c.execute('DELETE FROM telemetry_files')
        c.execute('DELETE FROM telemetry_measures')
        self.conn.commit()
        self.conn.close()
