from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import AnimalModel

class analizarImagenSerializer(serializers.ModelSerializer):
    imagenAnimal = serializers.SerializerMethodField()
    class Meta:
        model = AnimalModel
        fields = '__all__'
