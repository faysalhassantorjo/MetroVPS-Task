from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from base.tasks import fetch_usd_to_bdt
from .models import ExchangeRateLog, Subscription
from django.http.response import JsonResponse

from api.views import fetch_data
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to dashboard or home
        else:
            return render(request, 'base/login.html', {'error': 'Invalid credentials'})

    return render(request, 'base/login.html')


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
   
    