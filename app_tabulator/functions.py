from django_project import sql_db
import datetime

def getTestsOfTestSampleForSpecificOrder(TestSampleIdent, OrderIdent):
    db = sql_db.openDB()
    allTestIdentsForTestSample = getAllTestIdentsForTestSample(TestSampleIdent, db)
    testCases = getTestsByTestIdentsForOrder(TestIdents=allTestIdentsForTestSample, OrderIdent=OrderIdent, db=db) 
    tests = addTestPackageIdentsToTest(tests=testCases, db=db)
    testPackages = list(tests.keys())
    testPackageStructure = getTestPackageStructure(testPackages=testPackages, db=db)    
    formattedTests, counterID, treeElementCounter = formatTestsForTable(tests=tests, testPackages=testPackageStructure, topTestPackageIndex='', db=db)    
    formattedTests = addTestsWithoutTestPackages(returnValue=formattedTests, tests=tests, counterID=counterID, testPackage='', treeElementCounter=treeElementCounter, db=db)
    sql_db.closeDB(db)
    return formattedTests, testCases

    
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
                    print(f"treeElement for getSubTestPackageChildren {treeElement}")
                    childs, counterID = getSubTestPackageChildren(testPackages, tests, db, topTestPackageIndex=subTestPackage, counterID=counterID, treeLevel=treeLevel+1, treeElement=subTreeElement)
                    if childs:
                        subPackageChildren.append(childs)
            print(f"treeElement for packageChildren {treeElement}")
            counterID += 1
            children, counterID = getTestPackageChildren(testPackage=topTestPackage, startID=counterID, tests=tests, db=db, treeLevel=treeLevel+1, treeElement=f"{treeElement}", subTreeElementCounterOffset=subTreeElementCounter)
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
    children, counterID = getTestPackageChildren(testPackage=topTestPackageIndex, startID=counterID, tests=tests, db=db, treeLevel=treeLevel+1, treeElement=treeElement, subTreeElementCounterOffset=subTreeElementCounter)
    returnValue = {
        'id': tmpStartID, 
        'testIdent': [], 
        'name':getTestPackageName(topTestPackageIndex, db),            
        'element': 'header',
        'treeLevel': treeLevel,
        'treeElement': f"{treeElement}",
        '_children': subPackageChildren+children} 
    return returnValue, counterID

def getTestPackageChildren(testPackage, startID, tests, db, treeLevel, treeElement, subTreeElementCounterOffset=0):
    children = []
    counterID = startID
    subTreeElementCounter = subTreeElementCounterOffset
        
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
                'protocolIdent': data[ppb]['ProtocolIdent'],
                'testIdent':  testIdent, 
                #'name': testFormattedName, 
                'name': testName, 
                'operator': data[ppb]['Operator'], 
                'invoiceType': data[ppb]['InvoiceType'], 
                'date': data[ppb]['Date'], 
                'start': data[ppb]['Start'], 
                'stop': data[ppb]['Stop'], 
                'totalTime': round(data[ppb]['TotalTime'],1), 
                'isTestFinished': data[ppb]['isTestFinished'],
                'comment': data[ppb]['Comment'],                 
                'element': 'ppb',
                'treeLevel': treeLevel,
                'treeElement': f"{subTreeElement}"
            })
    return children, counterID

def addTestsWithoutTestPackages(returnValue, tests, counterID, testPackage, treeElementCounter, db):
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
        #data = {0: {'id': 1, 'testIdent': [], 'name': 'DIN EN IEC 61000-6-4:2020-09 [#37]', 'element': 'header', 'treeLevel': 0, 'treeElement': '1', '_children': [{'id': 3, 'testIdent': 2484, 'name': 'TE01 - DIN EN IEC 61000-6-4:2020-09 - CE [Unsym. Spannungen / LISN] [0,15 - 30 MHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-1', '_children': [{'id': 4, 'ProtocolIdent': 1015, 'TestIdent': 2484, 'name': 'TE01', 'Operator': 'ml', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 27), 'Start': datetime.time(10, 0), 'Stop': datetime.time(11, 0), 'TotalTime': 1.0, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-1-1'}]}, {'id': 5, 'testIdent': 2485, 'name': 'TE02 - DIN EN 55032:2016-02 - CE [Asym. Spannungen / Telekommikationsanschluss] [0,15 - 30 MHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-2', '_children': [{'id': 6, 'ProtocolIdent': 1016, 'TestIdent': 2485, 'name': 'TE02', 'Operator': 'ml', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 27), 'Start': datetime.time(11, 0), 'Stop': datetime.time(11, 20), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-2-1'}]}, {'id': 7, 'testIdent': 2486, 'name': 'TE03 - DIN EN IEC 61000-6-4:2020-09 - RE [gestrahlte Störgrößen][30 - 1000 MHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-3', '_children': [{'id': 8, 'ProtocolIdent': 976, 'TestIdent': 2486, 'name': 'TE03', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 25), 'Start': datetime.time(17, 0), 'Stop': datetime.time(19, 0), 'TotalTime': 2.0, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-3-1'}, {'id': 9, 'ProtocolIdent': 1011, 'TestIdent': 2486, 'name': 'TE03', 'Operator': 'sv', 'InvoiceType': 0, 'Date': datetime.date(2021, 10, 26), 'Start': datetime.time(18, 15), 'Stop': datetime.time(19, 0), 'TotalTime': 1.0, 'isTestFinished': True, 'Comment': 'Untersuchungen, da Fail', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-3-2'}]}, {'id': 10, 'testIdent': 2487, 'name': 'TE04 - DIN EN IEC 61000-6-4:2020-09  - RE [gestrahlte Störgrößen] [1 - 6 GHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-4', '_children': [{'id': 11, 'ProtocolIdent': 986, 'TestIdent': 2487, 'name': 'TE04', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 25), 'Start': datetime.time(19, 0), 'Stop': datetime.time(19, 30), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': 'Nur "kurz" angetestet, da <1GHz schon fail war', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-4-1'}]}]}, 1: {'id': 1, 'testIdent': [], 'name': 'DIN EN IEC 61000-6-2:2019-11 [#5]', 'element': 'header', 'treeLevel': 0, 'treeElement': '2', '_children': [{'id': 13, 'testIdent': 2488, 'name': 'TE05 - DIN EN 61000-4-2:2009-12 - CI [elektrostatische Entladung][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-1', '_children': [{'id': 14, 'ProtocolIdent': 1021, 'TestIdent': 2488, 'name': 'TE05', 'Operator': 'ml', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 27), 'Start': datetime.time(13, 0), 'Stop': datetime.time(13, 30), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-1-1'}]}, {'id': 15, 'testIdent': 2489, 'name': 'TE06 - DIN EN 61000-4-3:2011-04 - RI [gestrahlte Störgrößen][80 - 1000 MHz][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-2', '_children': [{'id': 16, 'ProtocolIdent': 883, 'TestIdent': 2489, 'name': 'TE06', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(11, 30), 'Stop': datetime.time(12, 0), 'TotalTime': 0.5, 'isTestFinished': False, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-2-1'}, {'id': 17, 'ProtocolIdent': 884, 'TestIdent': 2489, 'name': 'TE06', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(12, 30), 'Stop': datetime.time(14, 0), 'TotalTime': 1.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-2-2'}]}, {'id': 18, 'testIdent': 2490, 'name': 'TE07 - DIN EN 61000-4-3:2011-04 - RI [gestrahlte Störgrößen][1,4 - 6 GHz][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-3', '_children': [{'id': 19, 'ProtocolIdent': 866, 'TestIdent': 2490, 'name': 'TE07', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(9, 0), 'Stop': datetime.time(11, 30), 'TotalTime': 2.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-3-1'}]}, {'id': 20, 'testIdent': 2491, 'name': 'TE08 - DIN EN 61000-4-4:2013-04 - CI [EFT][DC][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-4', '_children': [{'id': 21, 'ProtocolIdent': 902, 'TestIdent': 2491, 'name': 'TE08', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(17, 0), 'Stop': datetime.time(17, 30), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-4-1'}]}, {'id': 22, 'testIdent': 2492, 'name': 'TE09 - DIN EN 61000-4-4:2013-04 - CI [EFT][Signalleitung][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-5', '_children': [{'id': 23, 'ProtocolIdent': 903, 'TestIdent': 2492, 'name': 'TE09', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(17, 45), 'Stop': datetime.time(18, 0), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-5-1'}]}, {'id': 24, 'testIdent': 2493, 'name': 'TE10 - DIN EN 61000-4-5:2015-03 - CI [Surge][DC unsym.][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-6', '_children': [{'id': 25, 'ProtocolIdent': 905, 'TestIdent': 2493, 'name': 'TE10', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(19, 0), 'Stop': datetime.time(19, 15), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-6-1'}]}, {'id': 26, 'testIdent': 2494, 'name': 'TE11 - DIN EN 61000-4-5:2015-03 - CI [Surge][DC sym.][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-7', '_children': [{'id': 27, 'ProtocolIdent': 904, 'TestIdent': 2494, 'name': 'TE11', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(18, 30), 'Stop': datetime.time(19, 0), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-7-1'}]}, {'id': 28, 'testIdent': 2495, 'name': 'TE12 - DIN EN 61000-4-5:2015-03 - CI [Surge][Signalleitung unsym.][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-8', '_children': [{'id': 29, 'ProtocolIdent': 906, 'TestIdent': 2495, 'name': 'TE12', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(19, 15), 'Stop': datetime.time(19, 30), 'TotalTime': 0.5, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-8-1'}]}, {'id': 30, 'testIdent': 2496, 'name': 'TE13 - DIN EN 61000-4-6:2014-08 - CI [geleitete Störgrößen][DC Supply][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-9', '_children': [{'id': 31, 'ProtocolIdent': 889, 'TestIdent': 2496, 'name': 'TE13', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(15, 0), 'Stop': datetime.time(15, 45), 'TotalTime': 1.0, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-9-1'}]}, {'id': 32, 'testIdent': 2497, 'name': 'TE14 - DIN EN 61000-4-6:2014-08 - CI [geleitete Störgrößen][Signalleitung][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-10', '_children': [{'id': 33, 'ProtocolIdent': 890, 'TestIdent': 2497, 'name': 'TE14', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 20), 'Start': datetime.time(15, 50), 'Stop': datetime.time(16, 45), 'TotalTime': 1.0, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-10-1'}]}, {'id': 34, 'testIdent': 2498, 'name': 'TE15 - Monitoring', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-11', '_children': [{'id': 35, 'ProtocolIdent': 1026, 'TestIdent': 2498, 'name': 'TE15', 'Operator': 'sv', 'InvoiceType': 1, 'Date': datetime.date(2021, 10, 27), 'Start': datetime.time(0, 0), 'Stop': datetime.time(0, 0), 'TotalTime': 0.0, 'isTestFinished': True, 'Comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-11-1'}]}]}, 2: {'id': 36, 'testIdent': 2499, 'name': 'TE16 - Ergebnisbericht nach DIN EN ISO/IEC 17025:2018-03 - EN - englisch', 'element': 'test', 'treeLevel': 0, 'treeElement': '3'}}
        data = {0: {'id': 1, 'testIdent': [], 'name': 'DIN EN IEC 61000-6-4:2020-09 [#37]', 'element': 'header', 'treeLevel': 0, 'treeElement': '1', '_children': [{'id': 3, 'testIdent': 2484, 'name': 'TE01 - DIN EN IEC 61000-6-4:2020-09 - CE [Unsym. Spannungen / LISN] [0,15 - 30 MHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-1', '_children': [{'id': 4, 'protocolIdent': 1015, 'testIdent': 2484, 'name': 'TE01', 'operator': 'ml', 'invoiceType': 1, 'date': datetime.date(2021, 10, 27), 'start': datetime.time(10, 0), 'stop': datetime.time(11, 0), 'totalTime': 1.0, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-1-1'}]}, {'id': 5, 'testIdent': 2485, 'name': 'TE02 - DIN EN 55032:2016-02 - CE [Asym. Spannungen / Telekommikationsanschluss] [0,15 - 30 MHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-2', '_children': [{'id': 6, 'protocolIdent': 1016, 'testIdent': 2485, 'name': 'TE02', 'operator': 'ml', 'invoiceType': 1, 'date': datetime.date(2021, 10, 27), 'start': datetime.time(11, 0), 'stop': datetime.time(11, 20), 'totalTime': 0.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-2-1'}]}, {'id': 7, 'testIdent': 2486, 'name': 'TE03 - DIN EN IEC 61000-6-4:2020-09 - RE [gestrahlte Störgrößen][30 - 1000 MHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-3', '_children': [{'id': 8, 'protocolIdent': 976, 'testIdent': 2486, 'name': 'TE03', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 25), 'start': datetime.time(17, 0), 'stop': datetime.time(19, 0), 'totalTime': 2.0, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-3-1'}, {'id': 9, 'protocolIdent': 1011, 'testIdent': 2486, 'name': 'TE03', 'operator': 'sv', 'invoiceType': 0, 'date': datetime.date(2021, 10, 26), 'start': datetime.time(18, 15), 'stop': datetime.time(19, 0), 'totalTime': 1.0, 'isTestFinished': True, 'comment': 'Untersuchungen, da Fail', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-3-2'}]}, {'id': 10, 'testIdent': 2487, 'name': 'TE04 - DIN EN IEC 61000-6-4:2020-09  - RE [gestrahlte Störgrößen] [1 - 6 GHz][#37]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-4', '_children': [{'id': 11, 'protocolIdent': 986, 'testIdent': 2487, 'name': 'TE04', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 25), 'start': datetime.time(19, 0), 'stop': datetime.time(19, 30), 'totalTime': 0.5, 'isTestFinished': True, 'comment': 'Nur "kurz" angetestet, da <1GHz schon fail war', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-4-1'}]}]}, 1: {'id': 1, 'testIdent': [], 'name': 'DIN EN IEC 61000-6-2:2019-11 [#5]', 'element': 'header', 'treeLevel': 0, 'treeElement': '2', '_children': [{'id': 13, 'testIdent': 2488, 'name': 'TE05 - DIN EN 61000-4-2:2009-12 - CI [elektrostatische Entladung][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-1', '_children': [{'id': 14, 'protocolIdent': 1021, 'testIdent': 2488, 'name': 'TE05', 'operator': 'ml', 'invoiceType': 1, 'date': datetime.date(2021, 10, 27), 'start': datetime.time(13, 0), 'stop': datetime.time(13, 30), 'totalTime': 0.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-1-1'}]}, {'id': 15, 'testIdent': 2489, 'name': 'TE06 - DIN EN 61000-4-3:2011-04 - RI [gestrahlte Störgrößen][80 - 1000 MHz][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-2', '_children': [{'id': 16, 'protocolIdent': 883, 'testIdent': 2489, 'name': 'TE06', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 20), 'start': datetime.time(11, 30), 'stop': datetime.time(12, 0), 'totalTime': 0.5, 'isTestFinished': False, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-2-1'}, {'id': 17, 'protocolIdent': 884, 'testIdent': 2489, 'name': 'TE06', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 20), 'start': datetime.time(12, 30), 'stop': datetime.time(14, 0), 'totalTime': 1.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-2-2'}]}, {'id': 18, 'testIdent': 2490, 'name': 'TE07 - DIN EN 61000-4-3:2011-04 - RI [gestrahlte Störgrößen][1,4 - 6 GHz][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-3', '_children': [{'id': 19, 'protocolIdent': 866, 'testIdent': 2490, 'name': 'TE07', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 20), 'start': datetime.time(9, 0), 'stop': datetime.time(11, 30), 'totalTime': 2.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-3-1'}]}, {'id': 20, 'testIdent': 2491, 'name': 'TE08 - DIN EN 61000-4-4:2013-04 - CI [EFT][DC][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-4', '_children': [{'id': 21, 'protocolIdent': 902, 'testIdent': 2491, 'name': 'TE08', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 20), 'start': datetime.time(17, 0), 'stop': datetime.time(17, 30), 'totalTime': 0.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-4-1'}]}, {'id': 22, 'testIdent': 2492, 'name': 'TE09 - DIN EN 61000-4-4:2013-04 - CI [EFT][Signalleitung][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-5', '_children': [{'id': 23, 'protocolIdent': 903, 'testIdent': 2492, 'name': 'TE09', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 20), 'start': datetime.time(17, 45), 'stop': datetime.time(18, 0), 'totalTime': 0.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-5-1'}]}, {'id': 24, 'testIdent': 2493, 'name': 'TE10 - DIN EN 61000-4-5:2015-03 - CI [Surge][DC unsym.][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-6', '_children': [{'id': 25, 'protocolIdent': 905, 'testIdent': 2493, 'name': 'TE10', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 20), 'start': datetime.time(19, 0), 'stop': datetime.time(19, 15), 'totalTime': 0.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-6-1'}]}, {'id': 26, 'testIdent': 2494, 'name': 'TE11 - DIN EN 61000-4-5:2015-03 - CI [Surge][DC sym.][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-7', '_children': [{'id': 27, 'protocolIdent': 904, 'testIdent': 2494, 'name': 'TE11', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 20), 'start': datetime.time(18, 30), 'stop': datetime.time(19, 0), 'totalTime': 0.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-7-1'}]}, {'id': 28, 'testIdent': 2495, 'name': 'TE12 - DIN EN 61000-4-5:2015-03 - CI [Surge][Signalleitung unsym.][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-8', '_children': [{'id': 29, 'protocolIdent': 906, 'testIdent': 2495, 'name': 'TE12', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 20), 'start': datetime.time(19, 15), 'stop': datetime.time(19, 30), 'totalTime': 0.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-8-1'}]}, {'id': 30, 'testIdent': 2496, 'name': 'TE13 - DIN EN 61000-4-6:2014-08 - CI [geleitete Störgrößen][DC Supply][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-9', '_children': [{'id': 31, 'protocolIdent': 889, 'testIdent': 2496, 'name': 'TE13', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 20), 'start': datetime.time(15, 0), 'stop': datetime.time(15, 45), 'totalTime': 1.0, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-9-1'}]}, {'id': 32, 'testIdent': 2497, 'name': 'TE14 - DIN EN 61000-4-6:2014-08 - CI [geleitete Störgrößen][Signalleitung][#5]', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-10', '_children': [{'id': 33, 'protocolIdent': 890, 'testIdent': 2497, 'name': 'TE14', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 20), 'start': datetime.time(15, 50), 'stop': datetime.time(16, 45), 'totalTime': 1.0, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-10-1'}]}, {'id': 34, 'testIdent': 2498, 'name': 'TE15 - Monitoring', 'element': 'test', 'treeLevel': 1, 'treeElement': '2-11', '_children': [{'id': 35, 'protocolIdent': 1026, 'testIdent': 2498, 'name': 'TE15', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 27), 'start': datetime.time(0, 0), 'stop': datetime.time(0, 0), 'totalTime': 0.0, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '2-11-1'}]}]}, 2: {'id': 36, 'testIdent': 2499, 'name': 'TE16 - Ergebnisbericht nach DIN EN ISO/IEC 17025:2018-03 - EN - englisch', 'element': 'test', 'treeLevel': 0, 'treeElement': '3'}}
        testCases = {2484: {'TestIdent': 2484, 'TestNumber': 1, 'Description': 'DIN EN IEC 61000-6-4:2020-09 - CE [Unsym. Spannungen / LISN] [0,15 - 30 MHz][#37]', 'TemplateIdent': 614}, 2485: {'TestIdent': 2485, 'TestNumber': 2, 'Description': 'DIN EN 55032:2016-02 - CE [Asym. Spannungen / Telekommikationsanschluss] [0,15 - 30 MHz][#37]', 'TemplateIdent': 612}, 2486: {'TestIdent': 2486, 'TestNumber': 3, 'Description': 'DIN EN IEC 61000-6-4:2020-09 - RE [gestrahlte Störgrößen][30 - 1000 MHz][#37]', 'TemplateIdent': 616}, 2487: {'TestIdent': 2487, 'TestNumber': 4, 'Description': 'DIN EN IEC 61000-6-4:2020-09  - RE [gestrahlte Störgrößen] [1 - 6 GHz][#37]', 'TemplateIdent': 615}, 2488: {'TestIdent': 2488, 'TestNumber': 5, 'Description': 'DIN EN 61000-4-2:2009-12 - CI [elektrostatische Entladung][#5]', 'TemplateIdent': 14}, 2489: {'TestIdent': 2489, 'TestNumber': 6, 'Description': 'DIN EN 61000-4-3:2011-04 - RI [gestrahlte Störgrößen][80 - 1000 MHz][#5]', 'TemplateIdent': 18}, 2490: {'TestIdent': 2490, 'TestNumber': 7, 'Description': 'DIN EN 61000-4-3:2011-04 - RI [gestrahlte Störgrößen][1,4 - 6 GHz][#5]', 'TemplateIdent': 185}, 2491: {'TestIdent': 2491, 'TestNumber': 8, 'Description': 'DIN EN 61000-4-4:2013-04 - CI [EFT][DC][#5]', 'TemplateIdent': 186}, 2492: {'TestIdent': 2492, 'TestNumber': 9, 'Description': 'DIN EN 61000-4-4:2013-04 - CI [EFT][Signalleitung][#5]', 'TemplateIdent': 187}, 2493: {'TestIdent': 2493, 'TestNumber': 10, 'Description': 'DIN EN 61000-4-5:2015-03 - CI [Surge][DC unsym.][#5]', 'TemplateIdent': 188}, 2494: {'TestIdent': 2494, 'TestNumber': 11, 'Description': 'DIN EN 61000-4-5:2015-03 - CI [Surge][DC sym.][#5]', 'TemplateIdent': 21}, 2495: {'TestIdent': 2495, 'TestNumber': 12, 'Description': 'DIN EN 61000-4-5:2015-03 - CI [Surge][Signalleitung unsym.][#5]', 'TemplateIdent': 191}, 2496: {'TestIdent': 2496, 'TestNumber': 13, 'Description': 'DIN EN 61000-4-6:2014-08 - CI [geleitete Störgrößen][DC Supply][#5]', 'TemplateIdent': 192}, 2497: {'TestIdent': 2497, 'TestNumber': 14, 'Description': 'DIN EN 61000-4-6:2014-08 - CI [geleitete Störgrößen][Signalleitung][#5]', 'TemplateIdent': 193}, 2498: {'TestIdent': 2498, 'TestNumber': 15, 'Description': 'Monitoring', 'TemplateIdent': 422}, 2499: {'TestIdent': 2499, 'TestNumber': 16, 'Description': 'Ergebnisbericht nach DIN EN ISO/IEC 17025:2018-03 - EN - englisch', 'TemplateIdent': 222}}
    if num == 1:
        data = {0: {'id': 1, 'testIdent': [], 'name': 'FCC Rules 47 CFT Part 15 - Subpart B - Unintentional radiators [#38]', 'element': 'header', 'treeLevel': 0, 'treeElement': '1', '_children': [{'id': 2, 'testIdent': [], 'name': '47 CFR Part 15 - [Gestrahlte Störgrößen] [#27]', 'element': 'header', 'treeLevel': 1, 'treeElement': '1-1', '_children': [{'id': 3, 'testIdent': 2137, 'name': 'TE02 - 47 CFR Part 15 - RE [E-Feld][Vormessung SAC 3m][30 - 1000 MHz][#27]', 'element': 'test', 'treeLevel': 2, 'treeElement': '1-1-1', '_children': [{'id': 4, 'protocolIdent': 685, 'testIdent': 2137, 'name': 'TE02', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 6), 'start': datetime.time(14, 45), 'stop': datetime.time(16, 30), 'totalTime': 2.0, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 3, 'treeElement': '1-1-1-1'}]}, {'id': 5, 'testIdent': 2138, 'name': 'TE03 - 47 CFR Part 15 - RE [E-Feld][Nachmessung OATS 10m][30 - 1000 MHz][#27]', 'element': 'test', 'treeLevel': 2, 'treeElement': '1-1-2', '_children': [{'id': 6, 'protocolIdent': 695, 'testIdent': 2138, 'name': 'TE03', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 7), 'start': datetime.time(10, 0), 'stop': datetime.time(11, 0), 'totalTime': 1.0, 'isTestFinished': False, 'comment': 'Aufbau', 'element': 'ppb', 'treeLevel': 3, 'treeElement': '1-1-2-1'}, {'id': 7, 'protocolIdent': 704, 'testIdent': 2138, 'name': 'TE03', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 7), 'start': datetime.time(11, 0), 'stop': datetime.time(12, 0), 'totalTime': 1.0, 'isTestFinished': False, 'comment': '', 'element': 'ppb', 'treeLevel': 3, 'treeElement': '1-1-2-2'}, {'id': 8, 'protocolIdent': 705, 'testIdent': 2138, 'name': 'TE03', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 7), 'start': datetime.time(13, 0), 'stop': datetime.time(14, 30), 'totalTime': 1.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 3, 'treeElement': '1-1-2-3'}]}, {'id': 9, 'testIdent': 2139, 'name': 'TE04 - 47 CFR Part 15 - RE [E-Feld][SAC 3m][1 - 5 GHz][#27]', 'element': 'test', 'treeLevel': 2, 'treeElement': '1-1-3', '_children': [{'id': 10, 'protocolIdent': 687, 'testIdent': 2139, 'name': 'TE04', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 6), 'start': datetime.time(17, 0), 'stop': datetime.time(17, 50), 'totalTime': 1.0, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 3, 'treeElement': '1-1-3-1'}]}]}, {'id': 12, 'testIdent': 2136, 'name': 'TE01 - 47 CFR Part 15 - CE [Geleitete Störgrößen] [0,15 - 30 MHz][#38]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-2', '_children': [{'id': 13, 'protocolIdent': 684, 'testIdent': 2136, 'name': 'TE01', 'operator': 'sv', 'invoiceType': 1, 'date': datetime.date(2021, 10, 6), 'start': datetime.time(8, 30), 'stop': datetime.time(12, 0), 'totalTime': 3.5, 'isTestFinished': True, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-2-1'}]}, {'id': 14, 'testIdent': 2140, 'name': 'TE05 - 47 CFR Part 15 - Zulassungsverfahren Certification CAB/USA [#38]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-3'}, {'id': 15, 'testIdent': 2141, 'name': 'TE06 - 47 CFR Part 15 - Zulassungskosten TCB - nach Aufwand [#38]', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-4'}, {'id': 16, 'testIdent': 2142, 'name': 'TE07 - Ergebnisbericht nach DIN EN ISO/IEC 17025:2018-03 - FCC - englisch', 'element': 'test', 'treeLevel': 1, 'treeElement': '1-5', '_children': [{'id': 17, 'protocolIdent': 750, 'testIdent': 2142, 'name': 'TE07', 'operator': 'sv', 'invoiceType': 0, 'date': datetime.date(2021, 10, 11), 'start': datetime.time(12, 0), 'stop': datetime.time(13, 0), 'totalTime': 1.0, 'isTestFinished': False, 'comment': '', 'element': 'ppb', 'treeLevel': 2, 'treeElement': '1-5-1'}]}]}}
        testCases = {2136: {'TestIdent': 2136, 'TestNumber': 1, 'Description': '47 CFR Part 15 - CE [Geleitete Störgrößen] [0,15 - 30 MHz][#38]', 'TemplateIdent': 620}, 2137: {'TestIdent': 2137, 'TestNumber': 2, 'Description': '47 CFR Part 15 - RE [E-Feld][Vormessung SAC 3m][30 - 1000 MHz][#27]', 'TemplateIdent': 482}, 2138: {'TestIdent': 2138, 'TestNumber': 3, 'Description': '47 CFR Part 15 - RE [E-Feld][Nachmessung OATS 10m][30 - 1000 MHz][#27]', 'TemplateIdent': 483}, 2139: {'TestIdent': 2139, 'TestNumber': 4, 'Description': '47 CFR Part 15 - RE [E-Feld][SAC 3m][1 - 5 GHz][#27]', 'TemplateIdent': 484}, 2140: {'TestIdent': 2140, 'TestNumber': 5, 'Description': '47 CFR Part 15 - Zulassungsverfahren Certification CAB/USA [#38]', 'TemplateIdent': 621}, 2141: {'TestIdent': 2141, 'TestNumber': 6, 'Description': '47 CFR Part 15 - Zulassungskosten TCB - nach Aufwand [#38]', 'TemplateIdent': 623}, 2142: {'TestIdent': 2142, 'TestNumber': 7, 'Description': 'Ergebnisbericht nach DIN EN ISO/IEC 17025:2018-03 - FCC - englisch', 'TemplateIdent': 224}}
    return data, testCases

