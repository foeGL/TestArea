from django_project import sql_db

def getTestsOfTestSampleForSpecificOrder(TestSampleIdent, OrderIdent):
    db = sql_db.openDB()
    allTestIdentsForTestSample = getAllTestIdentsForTestSample(TestSampleIdent, db)
    allTestForTestSample = []
    newTestIdents = []
    if allTestIdentsForTestSample:
        allTestForTestSample, newTestIdents = getTestsByTestIdents(allTestIdentsForTestSample, OrderIdent, db)
    sql_db.closeDB(db)
    return newTestIdents, allTestForTestSample

    
def getAllTestIdentsForTestSample(TestSampleIdent, db):
    table = 'TCPD_OrderAssignments'
    values = ['SourceIdent']
    where = f"SourceObjectClass='Test' AND AssignedObjectClass='TestSample' AND AssignedIdent={TestSampleIdent}"
    dictKey = 'SourceIdent'
    data = sql_db.readFromTable(db=db, table=table, values=values, where=where, dictKey=dictKey)
    return sorted(list(data.keys()))

def getTestsByTestIdents(TestIdents, OrderIdent, db):
    newTestIdents = []
    table = 'TCPD_Tests'
    values = ['TestIdent', 'TestNumber', 'Description', 'TemplateIdent']
    if len(TestIdents)>1:
        where = f"OrderIdent={OrderIdent} AND (TestIdent={' OR TestIdent='.join(str(x) for x in TestIdents)})"
    else:
        where = f"OrderIdent={OrderIdent} AND TestIdent={TestIdents[0]}"
    data = sql_db.readFromTable(db=db, table=table, values=values, where=where)
    tests = {}
    for key in data:        
        line = data[key]      
        id = line['TestIdent']
        name = f"TE{'{0:0=2d}'.format(line['TestNumber'])}"
        standard = getStandardForTest(db=db, TemplateIdent=line['TemplateIdent'])
        tests[id] = {'name': name, 'formatted': f"{name} - {line['Description']}", 'standard': standard}
        newTestIdents.append(id)
    return tests, newTestIdents

def getStandardForTest(db, TemplateIdent):
    table = 'TCPD_TestPlanTemplates'
    values = ['StandardIdent']
    where = f"TemplateIdent={TemplateIdent}"
    data = sql_db.readFromTable(db=db, table=table, values=values, where=where)
    
    if data[0]['StandardIdent']:
        table = 'TCPD_Standards'
        values = ['StandardDescription']
        where = f"StandardIdent={data[0]['StandardIdent']}"
        data = sql_db.readFromTable(db=db, table=table, values=values, where=where)
        return data[0]['StandardDescription']
    else:
        return ""


def getTestData():
    print("starte")
    tests = {
        2136: {
            'name': 'TE01',
            'formatted': 'TE01 - 47 CFR Part 15 - CE [Geleitete Störgrößen] [0,15 - 30 MHz][#38]',
            'standard': '47 CFR Part 15 Subpart B'}, 
        2137: {
            'name': 'TE02',
            'formatted': 'TE02 - 47 CFR Part 15 - RE [E-Feld][Vormessung SAC 3m][30 - 1000 MHz][#27]',
            'standard': '47 CFR Part 15 Subpart B'},
        2138: {
            'name': 'TE03',
            'formatted': 'TE03 - 47 CFR Part 15 - RE [E-Feld][Nachmessung OATS 10m][30 - 1000 MHz][#27]',
            'standard': '47 CFR Part 15 Subpart B'},
        2139: {
            'name': 'TE04',
            'formatted': 'TE04 - 47 CFR Part 15 - RE [E-Feld][SAC 3m][1 - 5 GHz][#27]',
            'standard': '47 CFR Part 15 Subpart B'},
        2140: {
            'name': 'TE05',
            'formatted': 'TE05 - 47 CFR Part 15 - Zulassungsverfahren Certification CAB/USA [#38]',
            'standard': '47 CFR Part 15 Subpart B'},
        2141: {
            'name': 'TE06',
            'formatted': 'TE06 - 47 CFR Part 15 - Zulassungskosten TCB - nach Aufwand [#38]',
            'standard': '47 CFR Part 15 Subpart B'},
        2142: {
            'name': 'TE07',
            'formatted': 'TE07 - Ergebnisbericht nach DIN EN ISO/IEC 17025:2018-03 - FCC - englisch',
            'standard': ''
            }
        }


    tableData = {
        0: {
            'ProtocolIdent': 684,
            'TestIdent': 2136,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279, 
            'Date': '2021-10-06',
            'Start': '08:30',
            'Stop': '12:00',
            'TotalTime': 3.5,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': True,
            'Comment': ''},
        1: {
            'ProtocolIdent': 685,
            'TestIdent': 2137,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-06',
            'Start': '14:45',
            'Stop': '16:30',
            'TotalTime': 2.0,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': True,
            'Comment': ''},
        2: {
            'ProtocolIdent': 695,
            'TestIdent': 2138,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-07',
            'Start': '10:00',
            'Stop': '11:00',
            'TotalTime': 1.0,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': False,
            'Comment': 'Aufbau'},
        3: {
            'ProtocolIdent': 704,
            'TestIdent': 2138,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-07',
            'Start': '11:00',
            'Stop': '12:00',
            'TotalTime': 1.0,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': False,
            'Comment': ''},
        4: {
            'ProtocolIdent': 705,
            'TestIdent': 2138,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-07',
            'Start': '13:00',
            'Stop': '14:30',
            'TotalTime': 1.5,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': True,
            'Comment': ''},
        5: {
            'ProtocolIdent': 687,
            'TestIdent': 2139,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-06',
            'Start': '17:00',
            'Stop': '17:50',
            'TotalTime': 1.0,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': True,
            'Comment': ''},
        6: {
            'ProtocolIdent': 750,
            'TestIdent': 2142,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-11',
            'Start': '00:00',
            'Stop': '00:00',
            'TotalTime': 0.0,
            'InvoiceType': 0,
            'InvoiceStatus': '',
            'isTestFinished': False,
            'Comment': ''}
        }

    return tests, tableData
