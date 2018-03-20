import unittest
import sqlite3

from ..uploadEDL import UploadEdl

class TestUpload(unittest.TestCase):
    
    conn = None
    smalljson = None
    jsonthree = None
    
    def setUp(self):
        
        # Connect to test db
        sqlite_file = 'telmon/test/telmon_test_db'
        self.conn = sqlite3.connect(sqlite_file)
        
        #load small json object
        file = open('telmon/test/small.json', 'r')
        self.smalljson = file.read()
        file.close()
        
        #load larger json object
        file = open('telmon/test/three.json', 'r')
        self.jsonthree = file.read()
        file.close()
 
    def test_loaddb(self):
        
        uploader = UploadEdl(self.conn, self.smalljson)
        self.conn.commit()
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM telemetry_files')
        retval = c.fetchall()
        val1 = retval[0][0]
        self.assertEqual(1, val1)
        c.execute('SELECT COUNT(*) FROM telemetry_measures')
        retval = c.fetchall()
        val1 = retval[0][0]
        self.assertEqual(1, val1)
 
    def test_loadthree(self):

        uploader = UploadEdl(self.conn, self.jsonthree)
        self.conn.commit()
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM telemetry_measures')
        retval = c.fetchall()
        val1 = retval[0][0]
        self.assertEqual(3, val1)      
 
    def tearDown(self):

        c = self.conn.cursor()
        c.execute('DELETE FROM telemetry_files')
        c.execute('DELETE FROM telemetry_measures')
        self.conn.commit()
        self.conn.close()
