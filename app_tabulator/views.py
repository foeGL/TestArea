from django.shortcuts import render
from . import functions

offline = True
numb = 2

TestOrders = {
    0: {'TestSampleIdent': 723, 'OrderIdent':469, 'Project': '21-0322'},
    1: {'TestSampleIdent': 674, 'OrderIdent':448, 'Project': '21-0331'},
    2: {'TestSampleIdent': 748, 'OrderIdent':500, 'Project': '21-0305'},
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