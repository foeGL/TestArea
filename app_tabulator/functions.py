from django_project import sql_db

def getTestsOfTestSampleForSpecificOrder(TestSampleIdent, OrderIdent):
    db = sql_db.openDB()
    allTestIdentsForTestSample = getAllTestIdentsForTestSample(TestSampleIdent, db)
    tests = getTestsByTestIdentsForOrder(TestIdents=allTestIdentsForTestSample, OrderIdent=OrderIdent, db=db)    
    tests = addTestPackageIdentsToTest(tests=tests, db=db)
    testPackages = list(tests.keys())
    testPackageStructure = getTestPackageStructure(testPackages=testPackages, db=db)    
    formattedTests, counterID = formatTestsForTable(tests=tests, testPackages=testPackageStructure, topTestPackageIndex='', db=db)    
    formattedTests = addTestsWithoutTestPackages(returnValue=formattedTests, tests=tests, counterID=counterID, testPackage='')
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
    if topTestPackageIndex in testPackages:
        tmpStartID = counterID
        for topTestPackage in testPackages[topTestPackageIndex]:
            if topTestPackage in testPackages:
                subPackageChildren = []
                for subTestPackage in testPackages[topTestPackage]:
                    childs, counterID = getSubTestPackageChildren(testPackages, tests, db, topTestPackageIndex=subTestPackage, counterID=counterID, treeLevel=treeLevel+1)
                    if childs:
                        subPackageChildren.append(childs)
                
            counterID += 1
            children, counterID = getTestPackageChildren(testPackage=topTestPackage, startID=counterID, tests=tests, db=db, treeLevel=treeLevel+1)
            returnValue[len(returnValue)] = {
                'id': tmpStartID, 
                'testIdent': [], 
                'name':getTestPackageName(topTestPackage, db),          
                'element': 'Header',
                'treeLevel': treeLevel,
                '_children': subPackageChildren+children} 
    return returnValue, counterID

def getSubTestPackageChildren(testPackages, tests, db, counterID, treeLevel, topTestPackageIndex=[]):
    returnValue = []
    counterID +=1
    tmpStartID = counterID
    subPackageChildren = []
    if topTestPackageIndex in testPackages:
        for subTestPackage in testPackages[topTestPackageIndex]:
            subPackageChildren.append(getSubTestPackageChildren(testPackages, tests, db, topTestPackageIndex=subTestPackage, treeLevel=treeLevel+1))
    children, counterID = getTestPackageChildren(testPackage=topTestPackageIndex, startID=counterID, tests=tests, db=db, treeLevel=treeLevel+1)
    returnValue = {
        'id': tmpStartID, 
        'testIdent': [], 
        'name':getTestPackageName(topTestPackageIndex, db),            
        'element': 'Header',
        'treeLevel': treeLevel,
        '_children': subPackageChildren+children} 
    return returnValue, counterID

def getTestPackageChildren(testPackage, startID, tests, db, treeLevel):
    children = []
    counterID = startID
    if testPackage in tests:
        for test in tests[testPackage]:
            counterID +=1
            tmpStartID = counterID
            testIdent = tests[testPackage][test]['TestIdent']
            name = f"TE{'{0:0=2d}'.format(tests[testPackage][test]['TestNumber'])}"
            formattedName = f"{name} - {tests[testPackage][test]['Description']}"
            ePPB, counterID = getEPPBForTest(testIdent=testIdent, counterID=counterID, db=db, testName=name, testFormattedName=formattedName, treeLevel=treeLevel+1)
            if ePPB:
                children.append({
                    "id": tmpStartID,  
                    "testIdent": testIdent,
                    "name": formattedName,           
                    'element': 'Test',
                    'treeLevel': treeLevel,
                    "_children": ePPB
                })
            else:
                children.append({
                    "id": tmpStartID,  
                    "testIdent": testIdent,
                    "name": formattedName,           
                    'element': 'Test',
                    'treeLevel': treeLevel
                })
    return children, counterID

def getEPPBForTest(testIdent, counterID, db, testName, testFormattedName, treeLevel):
    table="TCPD_WebGUI"
    where = f"TestIdent={testIdent}"
    order_by = {'Date':'ASC', 'Start': 'ASC'}
    data = sql_db.readFromTable(db=db, table=table, where=where, order_by=order_by)
    children = []
    if data:
        for ppb in data:
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
                'element': 'PPB',
                'treeLevel': treeLevel
            })
    return children, counterID

def addTestsWithoutTestPackages(returnValue, tests, counterID, testPackage):
    if testPackage in tests:
        for test in tests[testPackage]:
            counterID +=1
            name = f"TE{'{0:0=2d}'.format(tests[testPackage][test]['TestNumber'])}"
            returnValue[len(returnValue)] = {
                "id": counterID,  
                "testIdent":tests[testPackage][test]['TestIdent'],
                "name": f"{name} - {tests[testPackage][test]['Description']}",
                'element': 'Test',
                'treeLevel': 0
            }
    return returnValue
