from django.shortcuts import render
from .models import Chat, Message
def index(request):
  if request.method == 'POST':
    print("Received data " + request.POST["textMessage"])
    myChat = Chat.objects.get(id=1)
    Message.objects.create(text=request.POST["textMessage"], chat=myChat, author=request.user, receiver=request.user)
  return render(request, 'chat/index.html', {'username': 'Admin'})
