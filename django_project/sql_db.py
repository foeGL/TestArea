#2021-10-14
import datetime
from . import confSQL
import pypyodbc

#-------------------------------------------------------------
def openDB(SERVER=[], DATABASE=[], UID=[], PWD=[]):    
    config = confSQL.getSQLConfig()
    if SERVER:
        config["SERVER"] = SERVER
    if DATABASE:
        config["DATABASE"] = DATABASE
    if UID:
        config["UID"] = UID
    if PWD:
        config["PWD"] = PWD
    connect = pypyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                        SERVER=' + config["SERVER"] + '; \
                        DATABASE=' + config["DATABASE"] + '; \
                        Trusted_Connection=no; \
                        UID=' + config["UID"] + '; \
                        PWD='+ config["PWD"] + ';')

    cursor = connect.cursor()
    database = {'connect': connect, 'cursor': cursor}
    return database
#--------------------------------------------------------------

#--------------------------------------------------------------
def closeDB(db):
    db['connect'].close()
#--------------------------------------------------------------

#--------------------------------------------------------------
def getFolderPaths():
    return confSQL.getFolderPaths()
#--------------------------------------------------------------

#--------------------------------------------------------------
def getMailConfig():
    return confSQL.getMailConfig()
#--------------------------------------------------------------


def getSysTableNames(db):
    table = "sys.Tables"
    values = ["name"]
    order_by = {"name":"ASC"}
    dictKey = "name"
    sysTableNames = readFromTable(db=db, table=table, values=values, order_by=order_by, dictKey=dictKey)

    return list(sysTableNames.keys())

def sql_qry(db, qry_string, debug=False, executeSQL=True):
    if debug:
        print(qry_string)
    if executeSQL:
        db["cursor"].execute(qry_string)
        return db["cursor"].fetchall()
    else:
        return []

def doesTableExist(db, table, debug=False, executeSQL=True):
    sql = f"IF EXISTS(SELECT * FROM	INFORMATION_SCHEMA.TABLES WHERE	TABLE_NAME = '{table}') SELECT 1 AS search_result ELSE SELECT 0 AS search_result;"
    if debug:
        print(sql)
    if executeSQL:
        db["cursor"].execute(sql)
        return db["cursor"].fetchall()
    else:
        return []

def getTableFields(db, table, debug=False, executeSQL=True):
    cellHeader = {}
    valuesHeader = ["name", "type"]
    valuesSQL = ["COLUMN_NAME", "DATA_TYPE"]
    valuesSQLite = valuesHeader
    try:
        sql = f"SELECT {', '.join(valuesSQL)} FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'"
    except:
        sql = f"select sqlite_version()"
        db["cursor"].execute(sql).fetchall()[0][0]
        sql = f"SELECT {', '.join(valuesSQLite)} FROM PRAGMA_TABLE_INFO('{table}')"
    if debug:
        print(sql)
    if executeSQL:
        db["cursor"].execute(sql)    
        data = db["cursor"].fetchall()
        if debug:
            print("--------------------------------data--------------------------------")
            print(data)
        tmp_cellHeader = packArrayWithKeysToDict(keys=valuesHeader, data=data)      
        if debug:
            print("--------------------------------tmp_cellHeader--------------------------------")
            print(tmp_cellHeader)
        cellHeader = formatDictWithNewKey(newKey='Name', dictionary=tmp_cellHeader)
        if debug:
            print("--------------------------------cellHeader--------------------------------")
            print(cellHeader)
    return cellHeader

def packArrayWithKeysToDict(keys, data):
    tmp_cellHeader = {}
    for line in data:
        for i in range(0,len(keys)):
            formattedKey = keys[i].capitalize()
            if i==0:
                tmp_cellHeader[len(tmp_cellHeader)] = {formattedKey: line[i]}
            else:
                tmp_cellHeader[len(tmp_cellHeader)-1][formattedKey] = line[i]
    return tmp_cellHeader

def readFromTable(db, table, values=["*"], where="", order_by=[], debug=False, executeSQL=True, dictKey=[], convertType=[]):
    # table = "TCPD_TableName"
    # values = ['SpaltenName1', 'SpaltenNamen2'] - Special: ['*'] or ['TOP 1 *'] -> Direkte Ausgabe aller spalten als DICT
    # where = "SpaltenName1='Wert_SpaltenName1' AND SpaltenName2='Wert_SpaltenName2' OR .... "
    # order_by = {'SpaltenName1': 'ASC', 'SpaltenNamen2': 'DESC', .....}
    # dictKey = "SpaltenName1" -> Es kann nur einen geben!
    # convertType = {'SpaltenName1': 'int', 'SpaltenName2', 'str', ...}
    distinct = False
    if "DISTINCT" in values[0]:
        distinct = True  
        tmp = values[0].split(' ')    
        values = tmp[1] 

    if "*" in values[0]: 
        cellHeader = list(getTableFields(db=db, table=table).keys())
    else:
        if distinct == True:
            cellHeader = [values]
        else:
            cellHeader = values

    sql = f"Select"
    if "*" not in values[0]:
        if distinct == True:   
            sql = f"{sql} DISTINCT {values} from {table}"
        else:
            cols = ''
            for value in values:
                if not cols:
                    cols = f"[{value}]"
                else:
                    cols = f"{cols}, [{value}]"
            sql = f"{sql} {cols} from {table}"
    else:
        sql = f"{sql} {values[0]} from {table}"

    if len(where) > 0:
        sql = f"{sql} WHERE {where}"

    if len(order_by) > 0:
        sql = f"{sql} ORDER BY"
        for step, element in enumerate(order_by):
            if step == 0:
                sql = f"{sql} {element} {order_by[element]}"
            else:
                sql = f"{sql}, {element} {order_by[element]}"
    if debug:
        print(sql)
    respond = {}
    if executeSQL:
        data = db["cursor"].execute(sql)
        for index, line in enumerate(data):
            sub_vers = {}
            for pos, cell in enumerate(line):
                if cell is not None:
                    if convertType and cellHeader[pos] in list(convertType.keys()):
                        sub_vers[cellHeader[pos]] = convertTypeFunction(value=cell, typeToConvert=convertType[cellHeader[pos]])
                    else:
                        sub_vers[cellHeader[pos]] = cell
                else:
                    sub_vers[cellHeader[pos]] = ""
            respond[index] = sub_vers
        # returns not the cursor but the values inside as a list
    
    respond = formatDictWithNewKey(dictionary=respond, newKey=dictKey)

    return respond

def formatDictWithNewKey(dictionary, newKey):
    returnValue = dictionary
    if newKey and isinstance(newKey, str) and dictionary and (newKey in list(dictionary[0].keys())):
        try:
            respond_tmp = {}
            for key in dictionary:
                respond_tmp[dictionary[key][newKey]] = dictionary[key]
            returnValue = respond_tmp
        except:
            print("formatDictWithNewKey conversion error")
    return returnValue

def convertTypeFunction(value, typeToConvert):
    returnValue = value
    try:
        if typeToConvert == 'int':
            returnValue = int(value)
        if typeToConvert == 'str':
            returnValue = str(value)       
    except:
        print(f"ConvertError: {value} konnte nich als {typeToConvert} formatiert werden!")
    return returnValue

def updateTable(db, table, values, where, debug=False, executeSQL=True):
    # table = "TCPD_TableName"
    # values = {'SpaltenName1': SpaltenValue1, 'SpaltenNamen2': SpaltenValue2}
    # where = "SpaltenName1='Wert_SpaltenName1' AND SpaltenName2='Wert_SpaltenName2' OR .... "

    sql = f"UPDATE {table} SET"
    for index, key in enumerate(values):
        data_tmp = values[key]
        if data_tmp != 'NULL' and intType(data_tmp) is False and 'FROMPARTS' not in data_tmp:
            data_tmp = f"'{data_tmp}'"
        if index > 0:
            sql = f"{sql}, {key}={data_tmp}"
        else:
            sql = f"{sql} {key}={data_tmp}"

    if len(where) > 0:
        sql = f"{sql} WHERE {where}"    
    if debug:
        print(sql)
    if executeSQL:
        db["cursor"].execute(sql)
        db["connect"].commit()


def insertTable(db, table, values, debug=False, executeSQL=True):
    # table = "TCPD_TableName"
    # values = {'SpaltenName1': SpaltenValue1, 'SpaltenNamen2': SpaltenValue2}
    categories = ""
    data = ""
    cellHeader = getTableFields(db=db, table=table)
    categories = f"[{'], ['.join(list(values.keys()))}]"
    data_tmp = checkInsertValuesForDB(cellHeader, values)
    data = ', '.join(data_tmp)

    sql = f"INSERT INTO {table} ({categories}) VALUES ({data})"
    if debug:
        print(sql)
    if executeSQL:
        db["cursor"].execute(sql)
        db["connect"].commit()

def checkInsertValuesForDB(cellHeader, values):
    sqlFunctions = ['CURRENT_TIMESTAMP', 'GETDATE()', 'GETUTCDATE()']
    sqlSpecialFields= ['datetime', 'date', 'time']
    data = []
    for key in values:
        value = values[key]
        expectedType = cellHeader[key]['Type'].lower()
        if not value or value == 'NULL':
            if expectedType in sqlSpecialFields:                
                data.append('NULL')
            else:
                data.append(f"''")
        else:
            if value in sqlFunctions:
                data.append(value)
            else:
                if expectedType == 'int':                
                    data.append(f"{value}")
                elif expectedType == 'float':                        
                    data.append(f"{float(value)}")
                elif expectedType == 'bit':
                    if value == True:                     
                        data.append(f"1")
                    elif value == False:                                         
                        data.append(f"0")
                    else:                                         
                        data.append(f"{value}")
                elif expectedType == 'nvarchar' or expectedType == 'varchar' or expectedType == 'text':
                    data.append(f"'{value}'")
                elif expectedType == 'datetime':
                    data.append(f"{sqlDateTime(value)}")
                elif expectedType == 'date':                
                    data.append(f"{sqlDate(value)}")
                elif expectedType == 'time':                
                    data.append(f"{sqlTime(value)[1]}")
                else:                
                    data.append(f"'{value}'")
    return data

def deleteFromTable(db, table, where, debug=False, executeSQL=True):
    sql = f"DELETE FROM {table} WHERE {where}"
    if debug:
        print(sql)
    if executeSQL:
        db["cursor"].execute(sql)
        db["connect"].commit()


def createTable(db, table, categories, debug=False, executeSQL=True):
    sql = f"CREATE TABLE dbo.{table} {categories}"
    if debug:
        print(sql)
    if executeSQL:
        db["cursor"].execute(sql)
        db["connect"].commit()


def sqlDateTime(value=None):
    # value = "2019-07-09 00:00:00" oder "" oder None
    if not value or value is None:
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)
        hour = str(datetime.datetime.now().hour)
        minute = str(datetime.datetime.now().minute)
        second = str(datetime.datetime.now().second)
        microsecond = str(0)
    else:
        if not isinstance(value, str):
            value = str(value)
        valueDT = value.split(' ')
        date = valueDT[0].split('-')
        time = valueDT[1].split(':')
        year = date[0]
        month = date[1]
        day = date[2]
        hour = time[0]
        minute = time[1]
        second_tmp = time[2].split('.')
        second = second_tmp[0]
        microsecond = str(0)
    dtime = 'DATETIMEFROMPARTS(' + year + ', ' + month + ', ' + day + ', ' + hour + ', ' + minute + ', ' + second + ', ' + microsecond + ')'
    return dtime


def sqlDate(date=None):
    # date = "2019-07-09" oder "" oder None
    if not date or date is None:
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)
    else:
        date_split = date.split("-")
        year = date_split[0]
        month = date_split[1]
        day = date_split[2]
    dtime = 'DATEFROMPARTS(' + year + ', ' + month + ', ' + day + ')'
    return dtime


def sqlTime(time=None):
    # time = "00:00:00" oder "" oder None
    if  not time or time is None:
        hours = str(datetime.datetime.now().hour)
        minutes = str(datetime.datetime.now().minute)
        seconds = str(datetime.datetime.now().second)
    else:
        time_split = time.split(":")
        hours = int(time_split[0])
        minutes = 0
        seconds = 0
        if len(time_split)>1:
            minutes = int(time_split[1])
        if len(time_split)>2:
            seconds = int(time_split[2])
    microseconds = str(0)

    hours = "{0:0=2d}".format(hours)
    minutes = "{0:0=2d}".format(minutes)
    seconds = "{0:0=2d}".format(seconds)

    dtime = [f"{hours}:{minutes}", f"TIMEFROMPARTS( {hours}, {minutes}, {seconds}, 0, 1)"]
    return dtime


def intType(var):
    try:
        int(var)
        return True
    except:
        return False
