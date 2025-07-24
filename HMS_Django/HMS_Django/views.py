from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def about(request):
    return HttpResponse("Hello, World. You are on the about page")

def contact(request):
    return HttpResponse("Hello, World. You are on the contact page")