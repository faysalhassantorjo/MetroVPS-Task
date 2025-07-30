from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
import requests
from datetime import datetime
from base.models import ExchangeRateLog
from django.db import transaction
from base.models import Plan, Subscription, ExchangeRateLog

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from decouple import config
from .models import *

from .serializers import SubscriptionSerializer,PlanSerializer,SubscriptionCreateSerializer, SubscriptionCancelSerializer, UserSerializer

class RegisterUser(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        
        if not serializer.is_valid():
            return Response({
                'status':403,
                'payload':serializer.errors
            })
        
        serializer.save()
        
        user = User.objects.get(username = serializer.data['username'])
        
        refreshToken = RefreshToken.for_user(user)
        
        return Response({
            'status':200,
            'payload':serializer.data,
            'refreshtoken': str(refreshToken),
            'access_token':str(refreshToken.access_token)
        })

from django.urls import reverse
@api_view(['GET'])
def api_list(request):
    return Response({
        "exchange_rate": request.build_absolute_uri(reverse('get_exchange_rate')),
        "subscribe": request.build_absolute_uri(reverse('subscribe')),
        "subscriptions": request.build_absolute_uri(reverse('subscriptions')),
        "cancel_subscription": request.build_absolute_uri(reverse('cancel_subscription')),
        "register": request.build_absolute_uri(reverse('register')),
    })

@api_view(['GET'])
def all_plans(request):
    plans =Plan.objects.all()
    serializer_obj = PlanSerializer(plans,many=True)
    
    return Response(serializer_obj.data) 
    
def fetch_data(base, target):
    key = config('API_KEY')
    url = f'https://v6.exchangerate-api.com/v6/{key}/latest/{base}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # raise error if status != 200
        data = response.json()

        rate = data['conversion_rates'][target]
        now = datetime.now()

        return {
            'base': base,
            'target': target,
            'rate': rate,
            'fetched_at': now,
        }

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch exchange rate: {e}")
    except KeyError:
        raise Exception(f"Currency '{target}' not found in API response.")


@api_view(['GET'])
def get_exchange_rate(request):
    base = request.GET.get('base')
    target = request.GET.get('target')

    if not base or not target:
        return Response(
            {'error': 'Both base and target currencies are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        rate_data = fetch_data(base, target)
        return Response(rate_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
@authentication_classes([SessionAuthentication,BasicAuthentication])
def subscribe(request):
    user = request.user
    
    serializer = SubscriptionCreateSerializer(data=request.data)
    if serializer.is_valid():
    
        with transaction.atomic():
                plan_id = serializer.validated_data['plan_id']
                plan = Plan.objects.get(id=plan_id)
                subscription,created = Subscription.objects.get_or_create(
                    plan=plan,
                    user=user
                )

                if not created:
                    return Response(
                        {'error': 'You already have an active subscription to this plan'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                return Response(
                        SubscriptionSerializer(subscription).data,
                        status=status.HTTP_201_CREATED
                    )
    return Response({'error':'someerror'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
@authentication_classes([SessionAuthentication,BasicAuthentication])
def subscriptions(request):
    user= request.user
    
    subscriptions = user.subscription_set.all()
    return Response(
        SubscriptionSerializer(subscriptions,many=True).data
    )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
@authentication_classes([SessionAuthentication,BasicAuthentication])
def cancel_subscription(request):
    serializer = SubscriptionCancelSerializer(data=request.data)
    if serializer.is_valid():
        subscription_id = serializer.validated_data['subscription_id']
        
        with transaction.atomic():
            try:
                subscription = Subscription.objects.select_for_update().get(
                    id=subscription_id,
                    user=request.user
                )
                
                if subscription.status != 'active':
                    return Response(
                        {'error': 'Subscription is not active'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                subscription.status = 'cancelled'
                subscription.save()
                
                return Response(
                    SubscriptionSerializer(subscription).data,
                    status=status.HTTP_200_OK
                )
                
            except Subscription.DoesNotExist:
                return Response(
                    {'error': 'Subscription not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
