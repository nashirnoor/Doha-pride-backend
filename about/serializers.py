from rest_framework import serializers
from .models import Statistic, Activity,Description

class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ['title', 'value']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['name', 'icon']

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['description']
