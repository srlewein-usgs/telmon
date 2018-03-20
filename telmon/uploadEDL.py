from json import loads

class UploadEdl:



    def __init__(self, connect, upjson):
        #placeholder for initialization
        cursor = connect.cursor()
        try:
            cursor.execute('select 1')
            results = cursor.fetchone()
            ret = results[0]
        except:
            print('ERROR IN CONNECTION')
            return 
        
        if upjson is None:
             raise ValueError('UploadEdl class requires a json object')
             return
        self.upload(cursor, upjson)
        
        # I think the caller should commit and close
        #connect.commit()

    
    def upload(self, cursor, upjson):
        
        j = loads(upjson)
        qstr = "INSERT INTO telemetry_files VALUES ('" + j['SOURCE'] +"', '"+ j['STATION'] +\
               "', '" + j['filename'] +"', '"+ j['filedtg'] +"')"
        cursor.execute(qstr)
        
        vqstr = ''
        print(j['timeanddatum'])
        for values in j['timeanddatum']:
            qstr = "('"  + j['SOURCE'] +"', '"+ j['STATION'] +\
               "', '" + j['DEVICE']  +"', '"+ j['OVERWRITE'] +\
               "', '" + values[0] +"', '"+ values[1] + "'),"
            vqstr = vqstr + qstr
        
        # remove the trailing comma        
        vqstr = vqstr[:-1]
        qstr = 'INSERT INTO telemetry_measures VALUES ' + vqstr
        print(qstr)
        
        cursor.execute(qstr)
              
        
    
        
    
