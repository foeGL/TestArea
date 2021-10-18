from django.shortcuts import render
from . import functions

TestOrders = {
    0: {'TestSampleIdent': 723, 'OrderIdent':469, 'Project': '21-0322'},
    1: {'TestSampleIdent': 674, 'OrderIdent':448, 'Project': '21-0331'},
}

# Create your views here.
def index(request):    
    numb = 1
    TestSampleIdent = TestOrders[numb]['TestSampleIdent']
    OrderIdent = TestOrders[numb]['OrderIdent']
    formattedTests = functions.getTestsOfTestSampleForSpecificOrder(TestSampleIdent=TestSampleIdent, OrderIdent=OrderIdent)
    data = {
        'tests': formattedTests, 
        'protocol': [],
    }
    return render(request, "app_tabulator/templates/index.html", data)