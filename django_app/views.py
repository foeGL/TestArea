from django.shortcuts import render#
import json

# Create your views here.
def index(request):
    return render(request, 'django_app/templates/index.html', {})

def pre_records(request):
    OrderId = request.POST.get('orderId')
    if OrderId == 'newOrder':
        OrderId = 22
    post_data = {'orderId': OrderId }
    request.post('django_app:records', data=json.dumps(post_data))

def records(request):
    OrderId = request.POST.get('orderId')
    return render(request, 'django_app/templates/records.html', {'OrderId': OrderId})