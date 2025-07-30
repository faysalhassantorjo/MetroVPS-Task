from celery import shared_task
from celery import Celery
import requests
from .models import ExchangeRateLog, Subscription
from datetime import datetime
from django.utils import timesince, timezone
import logging
from decouple import config

logger = logging.getLogger(__name__)


@shared_task
def fetch_usd_to_bdt():
    key = config('API_KEY')
    url = f'https://v6.exchangerate-api.com/v6/{key}/latest/USD'
    
    try:
        response = requests.get(url)
        data = response.json()
        rate = data['conversion_rates']['BDT']
        ExchangeRateLog.objects.create(
            base_currency='USD',
            target_currency='BDT',
            rate=rate,
            fetched_at=datetime.now()
        )
    except Exception as e:
        print(f"Failed to fetch exchange rate: {e}")

@shared_task
def update_subscriptions():
    try:
        expired_count = Subscription.objects.filter(
            status='active',
            end_date__lt=timezone.now()
        ).update(status='expired')
        
        logger.info(f"Updated {expired_count} expired subscriptions")
        return f"Updated {expired_count} expired subscriptions"
    except Exception as e:
        logger.error(f"Failed to update expired subscriptions: {str(e)}")
        return f"Error: {str(e)}"
