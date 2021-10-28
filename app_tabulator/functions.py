from django_project import sql_db
import datetime

def getTestsOfTestSampleForSpecificOrder(TestSampleIdent, OrderIdent):
    db = sql_db.openDB()
    allTestIdentsForTestSample = getAllTestIdentsForTestSample(TestSampleIdent, db)
    tests = getTestsByTestIdentsForOrder(TestIdents=allTestIdentsForTestSample, OrderIdent=OrderIdent, db=db)    
    tests = addTestPackageIdentsToTest(tests=tests, db=db)
    testPackages = list(tests.keys())
    testPackageStructure = getTestPackageStructure(testPackages=testPackages, db=db)    
    formattedTests, counterID, treeElementCounter = formatTestsForTable(tests=tests, testPackages=testPackageStructure, topTestPackageIndex='', db=db)    
    formattedTests = addTestsWithoutTestPackages(returnValue=formattedTests, tests=tests, counterID=counterID, testPackage='', treeElementCounter=treeElementCounter, db=db)
    sql_db.closeDB(db)
    return formattedTests

    
def getAllTestIdentsForTestSample(TestSampleIdent, db):
    table = 'TCPD_OrderAssignments'
    values = ['SourceIdent']
    where = f"SourceObjectClass='Test' AND AssignedObjectClass='TestSample' AND AssignedIdent={TestSampleIdent}"
    dictKey = 'SourceIdent'
    data = sql_db.readFromTable(db=db, table=table, values=values, where=where, dictKey=dictKey)
    return sorted(list(data.keys()))

def getTestsByTestIdentsForOrder(TestIdents, OrderIdent, db):
    if TestIdents:
        table = 'TCPD_Tests'
        values = ['TestIdent', 'TestNumber', 'Description', 'TemplateIdent']
        if len(TestIdents)>1:
            where = f"OrderIdent={OrderIdent} AND (TestIdent={' OR TestIdent='.join(map(str, TestIdents))})"
        else:
            where = f"OrderIdent={OrderIdent} AND TestIdent={TestIdents[0]}"
        dictKey = 'TestIdent'
        data = sql_db.readFromTable(db=db, table=table, values=values, where=where, dictKey=dictKey)
    return data

def addTestPackageIdentsToTest(tests, db):
    testswithTestPackages = {}
    for testIdent in tests:        
        testPackage = getTestPackageForTest(db=db, TestIdent=testIdent)
        if testPackage:
            if testPackage not in testswithTestPackages:
                testswithTestPackages[testPackage] = {testIdent:tests[testIdent]}
            else:
                testswithTestPackages[testPackage][testIdent] = tests[testIdent]
        else:
            if '' not in testswithTestPackages:
                testswithTestPackages[''] = {testIdent:tests[testIdent]}
            else:
                testswithTestPackages[''][testIdent] = tests[testIdent]
    return testswithTestPackages


def getTestPackageForTest(db, TestIdent):
    table = 'TCPD_TestStructures'
    values = ['SourceIdent']
    where = f"AssignedObjectClass='Test' AND AssignedIdent={TestIdent} AND SourceObjectClass='TestPackage'"
    data = sql_db.readFromTable(db=db, table=table, values=values, where=where)
    if data:
        return data[0]['SourceIdent']
    else:
        return []

def getTestPackageName(TestPackageIdent, db):
    if TestPackageIdent:
        table = 'TCPD_TestPackages'
        values = ['Description']
        where = f"TestPackageIdent={TestPackageIdent}"
        data = sql_db.readFromTable(db=db, table=table, values=values, where=where)
        return data[0]['Description']
    else:
        return []


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

def getTestPackageStructure(testPackages, db):    
    structure = {}
    table = 'TCPD_TestStructures'
    values = ['SourceIdent']
    for testPackage in testPackages:
        if not testPackage == '':
            where = f"SourceObjectClass='TestPackage' AND AssignedObjectClass='TestPackage' AND AssignedIdent={testPackage}"
            data = sql_db.readFromTable(db=db, table=table, values=values, where=where)
            if not data:
                if '' not in structure:
                    tmp = [testPackage]
                else:
                    tmp = structure['']
                    tmp.append(testPackage)
                structure[''] = tmp
            else:
                key = data[0]['SourceIdent']
                if key not in structure:
                    tmp = [testPackage]
                else:
                    tmp = structure[key]
                    tmp.append(testPackage)
                structure[key] = tmp
    return structure

def formatTestsForTable(testPackages, tests, db, topTestPackageIndex=[]): 
    subPackageChildren = []
    counterID = 1
    treeLevel = 0
    returnValue = {}
    treeElement = 0
    if topTestPackageIndex in testPackages:
        tmpStartID = counterID
        for topTestPackage in testPackages[topTestPackageIndex]:
            subTreeElementCounter = 0
            treeElement +=1
            if topTestPackage in testPackages:
                subPackageChildren = []
                for subTestPackage in testPackages[topTestPackage]:
                    subTreeElementCounter += 1
                    subTreeElement = f"{treeElement}-{subTreeElementCounter}"
                    childs, counterID = getSubTestPackageChildren(testPackages, tests, db, topTestPackageIndex=subTestPackage, counterID=counterID, treeLevel=treeLevel+1, treeElement=subTreeElement)
                    if childs:
                        subPackageChildren.append(childs)
                
            counterID += 1
            children, counterID = getTestPackageChildren(testPackage=topTestPackage, startID=counterID, tests=tests, db=db, treeLevel=treeLevel+1, treeElement=f"{treeElement}")
            returnValue[len(returnValue)] = {
                'id': tmpStartID, 
                'testIdent': [], 
                'name':getTestPackageName(topTestPackage, db),          
                'element': 'header',
                'treeLevel': treeLevel,
                'treeElement': f"{treeElement}",
                '_children': subPackageChildren+children} 
    return returnValue, counterID, treeElement

def getSubTestPackageChildren(testPackages, tests, db, counterID, treeLevel, treeElement, topTestPackageIndex=[]):
    returnValue = []
    counterID +=1
    tmpStartID = counterID
    subPackageChildren = []
    subTreeElementCounter = 0
    if topTestPackageIndex in testPackages:
        for subTestPackage in testPackages[topTestPackageIndex]:
            subTreeElementCounter +=1            
            subTreeElement = f"{treeElement}-{subTreeElementCounter}"
            subPackageChildren.append(getSubTestPackageChildren(testPackages, tests, db, topTestPackageIndex=subTestPackage, treeLevel=treeLevel+1, treeElement=subTreeElement))
    children, counterID = getTestPackageChildren(testPackage=topTestPackageIndex, startID=counterID, tests=tests, db=db, treeLevel=treeLevel+1, treeElement=treeElement)
    returnValue = {
        'id': tmpStartID, 
        'testIdent': [], 
        'name':getTestPackageName(topTestPackageIndex, db),            
        'element': 'header',
        'treeLevel': treeLevel,
        'treeElement': f"{treeElement}",
        '_children': subPackageChildren+children} 
    return returnValue, counterID

def getTestPackageChildren(testPackage, startID, tests, db, treeLevel, treeElement):
    children = []
    counterID = startID
    subTreeElementCounter = 0
        
    if testPackage in tests:
        for test in tests[testPackage]:
            subTreeElementCounter += 1
            subTreeElement = f"{treeElement}-{subTreeElementCounter}"
            counterID +=1
            tmpStartID = counterID
            testIdent = tests[testPackage][test]['TestIdent']
            name = f"TE{'{0:0=2d}'.format(tests[testPackage][test]['TestNumber'])}"
            formattedName = f"{name} - {tests[testPackage][test]['Description']}"
            ePPB, counterID = getEPPBForTest(testIdent=testIdent, counterID=counterID, db=db, testName=name, testFormattedName=formattedName, treeLevel=treeLevel+1, treeElement=subTreeElement)
            newChild = {
                "id": tmpStartID,  
                "testIdent": testIdent,
                "name": formattedName,           
                'element': 'test',
                'treeLevel': treeLevel,
                'treeElement': f"{subTreeElement}",
            }
            if ePPB:
                newChild["_children"] = ePPB
            children.append(newChild)
    return children, counterID	

def getEPPBForTest(testIdent, counterID, db, testName, testFormattedName, treeLevel, treeElement):
    table="TCPD_WebGUI"
    where = f"TestIdent={testIdent}"
    order_by = {'Date':'ASC', 'Start': 'ASC'}
    data = sql_db.readFromTable(db=db, table=table, where=where, order_by=order_by)
    children = []
    if data:
        subTreeElementCounter = 0
        for ppb in data:
            subTreeElementCounter += 1
            subTreeElement = f"{treeElement}-{subTreeElementCounter}"
            counterID +=1
            children.append({
                'id': counterID,
                'ProtocolIdent': data[ppb]['ProtocolIdent'],
                'TestIdent':  testIdent, 
                #'name': testFormattedName, 
                'name': testName, 
                'Operator': data[ppb]['Operator'], 
                'InvoiceType': data[ppb]['InvoiceType'], 
                'Date': data[ppb]['Date'], 
                'Start': data[ppb]['Start'], 
                'Stop': data[ppb]['Stop'], 
                'TotalTime': round(data[ppb]['TotalTime'],1), 
                'isTestFinished': data[ppb]['isTestFinished'],
                'Comment': data[ppb]['Comment'],                 
                'element': 'ppb',
                'treeLevel': treeLevel,
                'treeElement': f"{subTreeElement}"
            })
    return children, counterID

def addTestsWithoutTestPackages(returnValue, tests, counterID, testPackage, treeElementCounter, db):
    print(tests)
    print(testPackage)
    if testPackage in tests:
        treeLevel = 0
        tmp_counter = treeElementCounter
        for test in tests[testPackage]:
            tmp_counter += 1
            counterID +=1
            name = f"TE{'{0:0=2d}'.format(tests[testPackage][test]['TestNumber'])}"
            formattedName = f"{name} - {tests[testPackage][test]['Description']}"
            testIdent = tests[testPackage][test]['TestIdent']
            subTreeElement = f"{tmp_counter}"
            ePPB, counterID = getEPPBForTest(testIdent=testIdent, counterID=counterID, db=db, testName=name, testFormattedName=formattedName, treeLevel=treeLevel+1, treeElement=subTreeElement)
            
            returnValue[len(returnValue)] = {
                "id": counterID,  
                "testIdent":testIdent,
                "name": formattedName,
                'element': 'test',
                'treeLevel': treeLevel,
                'treeElement': subTreeElement
            }

            if ePPB:
                returnValue[len(returnValue)-1]["_children"] = ePPB

    return returnValue



def getTestValues(num):
    if num == 2:
        data = {0: {'id': 1, 'testIdent': [], 'name': 'DIN EN IEC 61000-6-4:2020-09 [#37]', 'element': 'header', 'treeLevel': 0, 'treeElement': '1', '_children': [{'id': 3, 'testIdent': 2484, 'name': 'TE01 - DIN EN IEC 61000-6-4:2020-09 - CE [Unsym. Spannungen / LISN] [0,15 - 30 MHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-1'}, {'id': 4, 'testIdent': 2485, 'name': 'TE02 - DIN EN 55032:2016-02 - CE [Asym. Spannungen / Telekommikationsanschluss] [0,15 - 30 MHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-2'}, {'id': 5, 'testIdent': 2486, 'name': 'TE03 - DIN EN IEC 61000-6-4:2020-09 - RE [gestrahlte Störgrößen][30 - 1000 MHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-3'}, {'id': 6, 'testIdent': 2487, 'name': 'TE04 - DIN EN IEC 61000-6-4:2020-09  - RE [gestrahlte Störgrößen] [1 - 6 GHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-4'}]}, 1: {'id': 1, 'testIdent': [], 'name': 'DIN EN IEC 61000-6-2:2019-11 [#5]', 'element': 'header', 'treeLevel': 0, 'treeElement': '2', '_children': [{'id': 8, 'testIdent': 2488, 'name': 'TE05 - DIN EN 61000-4-2:2009-12 - CI [elektrostatische Entladung][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-1'}, {'id': 9, 'testIdent': 2489, 'name': 'TE06 - DIN EN 61000-4-3:2011-04 - RI [gestrahlte Störgrößen][80 - 1000 MHz][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-2', '_children': [{'id': 10, 'ProtocolIdent': 883, 'TestIdent': 2489, 'name': 'TE06', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(11, 30), 'Stop': datetime.time(12, 0), 'TotalTime': 0.5, 'isTestFinished': False, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-2-1'}, {'id': 11, 'ProtocolIdent': 884, 'TestIdent': 2489, 'name': 'TE06', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(12, 30), 'Stop': datetime.time(14, 0), 'TotalTime': 1.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-2-2'}]}, {'id': 12, 'testIdent': 2490, 'name': 'TE07 - DIN EN 61000-4-3:2011-04 - RI [gestrahlte Störgrößen][1,4 - 6 GHz][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-3', '_children': [{'id': 13, 'ProtocolIdent': 866, 'TestIdent': 2490, 'name': 'TE07', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(9, 0), 'Stop': datetime.time(11, 30), 'TotalTime': 2.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-3-1'}]}, {'id': 14, 'testIdent': 2491, 'name': 'TE08 - DIN EN 61000-4-4:2013-04 - CI [EFT][DC][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-4', '_children': [{'id': 15, 'ProtocolIdent': 902, 'TestIdent': 2491, 'name': 'TE08', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(17, 0), 'Stop': datetime.time(17, 30), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-4-1'}]}, {'id': 16, 'testIdent': 2492, 'name': 'TE09 - DIN EN 61000-4-4:2013-04 - CI [EFT][Signalleitung][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-5', '_children': [{'id': 17, 'ProtocolIdent': 903, 'TestIdent': 2492, 'name': 'TE09', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(17, 45), 'Stop': datetime.time(18, 0), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-5-1'}]}, {'id': 18, 'testIdent': 2493, 'name': 'TE10 - DIN EN 61000-4-5:2015-03 - CI [Surge][DC unsym.][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-6', '_children': [{'id': 19, 'ProtocolIdent': 905, 'TestIdent': 2493, 'name': 'TE10', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(19, 0), 'Stop': datetime.time(19, 15), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-6-1'}]}, {'id': 20, 'testIdent': 2494, 'name': 'TE11 - DIN EN 61000-4-5:2015-03 - CI [Surge][DC sym.][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-7', '_children': [{'id': 21, 'ProtocolIdent': 904, 'TestIdent': 2494, 'name': 'TE11', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(18, 30), 'Stop': datetime.time(19, 0), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-7-1'}]}, {'id': 22, 'testIdent': 2495, 'name': 'TE12 - DIN EN 61000-4-5:2015-03 - CI [Surge][Signalleitung unsym.][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-8', '_children': [{'id': 23, 'ProtocolIdent': 906, 'TestIdent': 2495, 'name': 'TE12', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(19, 15), 'Stop': datetime.time(19, 30), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-8-1'}]}, {'id': 24, 'testIdent': 2496, 'name': 'TE13 - DIN EN 61000-4-6:2014-08 - CI [geleitete Störgrößen][DC Supply][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-9', '_children': [{'id': 25, 'ProtocolIdent': 889, 'TestIdent': 2496, 'name': 'TE13', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(15, 0), 'Stop': datetime.time(15, 45), 'TotalTime': 1.0, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-9-1'}]}, {'id': 26, 'testIdent': 2497, 'name': 'TE14 - DIN EN 61000-4-6:2014-08 - CI [geleitete Störgrößen][Signalleitung][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-10', '_children': [{'id': 27, 'ProtocolIdent': 890, 'TestIdent': 2497, 'name': 'TE14', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(15, 50), 'Stop': datetime.time(16, 45), 'TotalTime': 1.0, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-10-1'}]}, {'id': 28, 'testIdent': 2498, 'name': 'TE15 - Monitoring', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-11'}]}, 2: {'id': 29, 'testIdent': 2499, 'name': 'TE16 - Ergebnisbericht nach DIN EN ISO/IEC 17025:2018-03 - EN - englisch', 'element': 'test', 'treeLevel': 0, 'treeElement': '3'}}
    if num == 1:
        data = {0: {'id': 1, 'testIdent': [], 'name': 'FCC Rules 47 CFT Part 15 - Subpart B - Unintentional radiators [#38]', 'element': 'header', 'treeLevel': 0, 'treeElement': 1, '_children': [{'id': 2, 'testIdent': [], 'name': '47 CFR Part 15 - [Gestrahlte Störgrößen] [#27]', 'element': 'header', 'treeLevel': 1, 'treeElement': '1-1', 'subTreeElement': ['1', '1-1'], '_children': [{'id': 3, 'testIdent': 2137, 'name': 'TE02 - 47 CFR Part 15 - RE [E-Feld][Vormessung SAC 3m][30 - 1000 MHz][#27]', 'element': 'test', 'treeLevel': 2, 'treeElement': '1-1-1', 'subTreeElement': ['1', '1-1'], '_children': [{'id': 4, 'ProtocolIdent': 685, 'TestIdent': 2137, 'name': 'TE02', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 6), 'Start': datetime.time(14, 45), 'Stop': datetime.time(16, 30), 'TotalTime': 2.0, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 3, 'treeElement': '1-1-1-1', 'subTreeElement': ['1', '1-1']}]}, {'id': 5, 'testIdent': 2138, 'name': 'TE03 - 47 CFR Part 15 - RE [E-Feld][Nachmessung OATS 10m][30 - 1000 MHz][#27]', 'element': 'test', 'treeLevel': 2, 'treeElement': '1-1-2', 'subTreeElement': ['1', '1-1'], '_children': [{'id': 6, 'ProtocolIdent': 695, 'TestIdent': 2138, 'name': 'TE03', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 7), 'Start': datetime.time(10, 0), 'Stop': datetime.time(11, 0), 'TotalTime': 1.0, 'isTestFinished': False, 'Comment': 'Aufbau', 'element': 'ppb', 'treeLevel': 3, 'treeElement': '1-1-2-1', 'subTreeElement': ['1', '1-1']}, {'id': 7, 'ProtocolIdent': 704, 'TestIdent': 2138, 'name': 'TE03', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 7), 'Start': datetime.time(11, 0), 'Stop': datetime.time(12, 0), 'TotalTime': 1.0, 'isTestFinished': False, 'Comment': '', 'element': 'ppb', 'treeLevel': 3, 'treeElement': '1-1-2-2', 'subTreeElement': ['1', '1-1']}, {'id': 8, 'ProtocolIdent': 705, 'TestIdent': 2138, 'name': 'TE03', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 7), 'Start': datetime.time(13, 0), 'Stop': datetime.time(14, 30), 'TotalTime': 1.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 3, 'treeElement': '1-1-2-3', 'subTreeElement': ['1', '1-1']}]}, {'id': 9, 'testIdent': 2139, 'name': 'TE04 - 47 CFR Part 15 - RE [E-Feld][SAC 3m][1 - 5 GHz][#27]', 'element': 'test', 'treeLevel': 2, 'treeElement': '1-1-3', 'subTreeElement': ['1', '1-1'], '_children': [{'id': 10, 'ProtocolIdent': 687, 'TestIdent': 2139, 'name': 'TE04', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 6), 'Start': datetime.time(17, 0), 'Stop': datetime.time(17, 50), 'TotalTime': 1.0, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 3, 'treeElement': '1-1-3-1', 'subTreeElement': ['1', '1-1']}]}]}, {'id': 12, 'testIdent': 2136, 'name': 'TE01 - 47 CFR Part 15 - CE [Geleitete Störgrößen] [0,15 - 30 MHz][#38]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-1', 'subTreeElement': ['1'], '_children': [{'id': 13, 'ProtocolIdent': 684, 'TestIdent': 2136, 'name': 'TE01', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 6), 'Start': datetime.time(8, 30), 'Stop': datetime.time(12, 0), 'TotalTime': 3.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-1-1', 'subTreeElement': ['1']}]}, {'id': 14, 'testIdent': 2140, 'name': 'TE05 - 47 CFR Part 15 - Zulassungsverfahren Certification CAB/USA [#38]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-2', 'subTreeElement': ['1']}, {'id': 15, 'testIdent': 2141, 'name': 'TE06 - 47 CFR Part 15 - Zulassungskosten TCB - nach Aufwand [#38]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-3', 'subTreeElement': ['1']}, {'id': 16, 'testIdent': 2142, 'name': 'TE07 - Ergebnisbericht nach DIN EN ISO/IEC 17025:2018-03 - FCC - englisch', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-4', 'subTreeElement': ['1'], '_children': [{'id': 17, 'ProtocolIdent': 750, 'TestIdent': 2142, 'name': 'TE07', 'Operator': 'sv', 'InvoiceType': 0, 'Date': datetime.date(2021, 10, 11), 'Start': datetime.time(12, 0), 'Stop': datetime.time(13, 0), 'TotalTime': 1.0, 'isTestFinished': False, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-4-1', 'subTreeElement': ['1']}]}]}}
    return data

