from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate as myAuthenticate
from django.contrib.auth import login as myLogin
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
import os
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
load_dotenv()

User = get_user_model()

class UserList(generics.ListCreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  lookup_field = 'slug'

@csrf_exempt
def authentication(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = myAuthenticate(request, email=email, password=password)
    if user is not None:
      myLogin(request, user)
      return HttpResponse(status=200)
    else:
      return HttpResponse(status=404)
  else:
    return HttpResponse(status=400)