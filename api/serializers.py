from rest_framework import serializers
from .models import ShotList, ConsentForm, Project

class ShotListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShotList
        fields = '__all__'

class ConsentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsentForm
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
