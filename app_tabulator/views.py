from django.shortcuts import render
from . import functions

offline = False
numb = 7

TestOrders = {
    0: {'TestSampleIdent': 723, 'OrderIdent':469, 'Project': '21-0322'},
    1: {'TestSampleIdent': 674, 'OrderIdent':448, 'Project': '21-0331'},
    2: {'TestSampleIdent': 748, 'OrderIdent':500, 'Project': '21-0305'},
    3: {'TestSampleIdent': 620, 'OrderIdent':456, 'Project': '21-0319'},
    4: {'TestSampleIdent': 621, 'OrderIdent':457, 'Project': '21-0319'},
    5: {'TestSampleIdent': 622, 'OrderIdent':458, 'Project': '21-0319'},
    6: {'TestSampleIdent': 623, 'OrderIdent':459, 'Project': '21-0319'},
    7: {'TestSampleIdent': 765, 'OrderIdent':521, 'Project': '21-0290'},


    
}

# Create your views here.
def index(request):  
    if offline:
        formattedTests = functions.getTestValues(numb)
    else:
        TestSampleIdent = TestOrders[numb]['TestSampleIdent']
        OrderIdent = TestOrders[numb]['OrderIdent']
        formattedTests = functions.getTestsOfTestSampleForSpecificOrder(TestSampleIdent=TestSampleIdent, OrderIdent=OrderIdent)
    data = {
        'tests': formattedTests, 
        'protocol': [],
    }
    return render(request, "app_tabulator/templates/index.html", data)