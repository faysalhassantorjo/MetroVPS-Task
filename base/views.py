from django.shortcuts import render
from django.http import HttpResponse
from base.tasks import fetch_usd_to_bdt
from .models import ExchangeRateLog, Subscription
from django.http.response import JsonResponse

from api.views import fetch_data
from django.contrib.auth.models import User

# Create your views here.

def rate_logs(request):
    
    logs = ExchangeRateLog.objects.order_by('-fetched_at')
    
 
    context ={
        'logs':logs
    }

    return render(request,'base/log.html',context)
    
    
def home(request):
    subscriptions = Subscription.objects.select_related('user', 'plan').all()

    context ={
        'subscriptions': subscriptions
    }
    return render(request, 'base/home.html',context)


def fatch_rate(request):
    if request.method == 'GET':
        base = request.GET.get('base')
        target = request.GET.get('target')
        response = fetch_data(base,target)
        
        return JsonResponse(response)
   
    