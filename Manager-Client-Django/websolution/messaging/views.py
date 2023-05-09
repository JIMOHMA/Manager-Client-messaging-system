from django.shortcuts import render
from .models import Message
from .forms import MessageForm
from .AppManager import AppManager
from .ClientApp import ClientApp
from .forms import MessageForm

def manager_view(request):
    context = {
        "userName":   "App 0 Manager", 
        "message":     "Welcome to my server" 
    }

    context["formManager"]  = MessageForm()

    myForm = MessageForm(request.POST or None)
    if (request.method  == "POST" and myForm.is_valid()):
        receivedMessage = myForm.cleaned_data.get("Message")

        print("The message sent is: ", receivedMessage)
        # save message received  inthe database and render all the messages in the database
        msgObject = Message()
        msgObject.userName = "App 0 Manager"
        msgObject.message  = receivedMessage
        msgObject.save()

        # Send the message through the zeroMQ socket connection

    # get all the messages in the database and send it to context
    allMessages = Message.objects.all()

    context["allMessages"] = allMessages
    return render(request, "manager.html", context=context)

def client_view(request):
    context = {
        "userName":   "client",
        "message":    "Requesting a file from the manager"
    }

    context['formClient'] = MessageForm()

    myForm = MessageForm(request.POST or None)
    if (request.method  == "POST" and myForm.is_valid()):
        receivedMessage = myForm.cleaned_data.get("Message")

        print("The message sent is: ", receivedMessage)
        # save message received  inthe database and render all the messages in the database
        msgObject = Message()
        msgObject.userName = "ClientApp"
        msgObject.message  = receivedMessage
        msgObject.save()

    # get all the messages in the database and send it to context
    allMessages = Message.objects.all()

    context["allMessages"] = allMessages
    return render(request, "client.html", context=context)

def sendtoClient(request, messageContext):

    return render(request, "client.html", context=messageContext)

# TODO: Implementing Channels
# https://realpython.com/getting-started-with-django-channels/