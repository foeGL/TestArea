from django.shortcuts import render
from . import functions

# Create your views here.
def index(request):    
    TestSampleIdent = 723
    OrderIdent = 469
    formattedTests = functions.getTestsOfTestSampleForSpecificOrder(TestSampleIdent=TestSampleIdent, OrderIdent=OrderIdent)
    data = {
        'tests': formattedTests, 
        'protocol': [],
    }
    print(formattedTests)
    return render(request, "app_tabulator/templates/index.html", data)