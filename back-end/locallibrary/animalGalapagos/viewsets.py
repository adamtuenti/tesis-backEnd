from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import AnimalModel
from .serializers import analizarImagenSerializer
from django.http import HttpResponse
from rest_framework.response import Response


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = AnimalModel.objects.all()
    serializer_class = analizarImagenSerializer