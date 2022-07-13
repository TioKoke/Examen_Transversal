from django.shortcuts import render
from .serializers import PerdiodistasSerializers
from rest_framework import generics
from WebCaosNews.models import UserProfile
# Create your views here.

class PeridistaViewSet(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = PerdiodistasSerializers
