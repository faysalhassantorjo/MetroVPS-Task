from rest_framework import serializers
from base.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PlanSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
        
class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = '__all__'
        
class SubscriptionCreateSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    
    def validate_plan_id(self, value):
        try:
            Plan.objects.get(id=value)
        except Plan.DoesNotExist:
            raise serializers.ValidationError("Plan does not exist")
        return value
    
class SubscriptionCancelSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()
    
    def validate_subscription_id(self, value):
        try:
            subscription = Subscription.objects.get(id=value)
            if subscription.status != 'active':
                raise serializers.ValidationError("Subscription is not active")
        except Subscription.DoesNotExist:
            raise serializers.ValidationError("Subscription does not exist")
        return value