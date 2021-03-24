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
from .forms import UserRegistrationForm
load_dotenv()

User = get_user_model()

@csrf_exempt
@api_view(['GET', 'POST'])
def userList(request):
  if request.method == "GET":
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == "POST":
    print(request.POST)
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      nickname = form.cleaned_data['nickname']
      gender = form.cleaned_data['gender']
      age = form.cleaned_data['age']
      ethnicity = form.cleaned_data['ethnicity']
      location = form.cleaned_data['location']
      fromFirebase = form.cleaned_data['fromFirebase']
      userPhotoURL = form.cleaned_data['userPhotoURL']
      password = form.cleaned_data['password']
      user = User(email=email, nickname=nickname,gender=gender, age=age, ethnicity=ethnicity,location=location, fromFirebase=fromFirebase,userPhotoURL=userPhotoURL)
      user.set_password(password)
      serializer = UserSerializer(data=model_to_dict(user))
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      print(serializer.error_messages)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    print(form.errors)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


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