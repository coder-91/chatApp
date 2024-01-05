from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth import authenticate, login

def index(request):
  if request.method == 'POST':
    print("Received data " + request.POST["textMessage"])
    myChat = Chat.objects.get(id=1)
    Message.objects.create(text=request.POST["textMessage"], chat=myChat, author=request.user, receiver=request.user)
  chatMessages = Message.objects.filter(chat__id=1)
  return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
      login(request, user)
      return HttpResponseRedirect('/chat/')
    else:
      return render(request, 'auth/login.html', {'wrongPassword': True})
  return render(request, 'auth/login.html')
