from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import weatherapi


class CustomGet(APIView):
    """
    A custom endpoint for GET request.
    """
    def index(request):
        return Response({'City': "Hello"})

    def get(self, request, format=None):
        """
        Return weather info
        """
        city = request.GET['city']
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        res = weatherapi.api_call(city, from_date, to_date)
        return Response(dict({'City': city, 'From date': from_date,
                        'To date': to_date}, **res))
