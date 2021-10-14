from django.shortcuts import render
from . import functions

# Create your views here.
def index(request):    
    TestSampleIdent = 723
    OrderIdent = 469
    [TestIdents, Tests] = functions.getTestsOfTestSampleForSpecificOrder(TestSampleIdent=TestSampleIdent, OrderIdent=OrderIdent)
    print(Tests)
    data = {
        'testIdents': TestIdents, 
        'tests': Tests, 
        'protocol': [],
    }
    return render(request, "app_tabulator/templates/index.html", data)