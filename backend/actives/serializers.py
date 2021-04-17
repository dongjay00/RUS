from rest_framework import serializers
from .models import Active, ActiveDetail


class ActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Active
        fields = '__all__'


class ActiveDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveDetail
        fields = '__all__'