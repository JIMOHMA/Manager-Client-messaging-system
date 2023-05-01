from django.shortcuts import render
from .models import Message


def manager(request):
    context = {
        "userName":   "App 0 Manager", 
        "message":     "Welcome to my server" 
    }
    return render(request, "manager.html", context=context)

def client(request):
    context = {
        "userName":   "client",
        "message":    "Requesting a file from the manager"
    }
    return render(request, "client.html", context=context)