from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/') #redirect when user is not logged in
def index(request):
  if request.method == 'POST':
    print("Received data " + request.POST["textMessage"])
    myChat = Chat.objects.get(id=1)
    Message.objects.create(text=request.POST["textMessage"], chat=myChat, author=request.user, receiver=request.user)
  chatMessages = Message.objects.filter(chat__id=1)
  return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
  redirect = request.GET.get('next')
  if request.method == 'POST':
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user:
      login(request, user)
      # Wenn die URL so aussieht: http://example.com/some-path/?next=/redirect-here/, dann würde request.GET.get('next') den Wert '/redirect-here/' zurückgeben.
      return HttpResponseRedirect(request.POST.get('redirect'))
    else:
      return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
  return render(request, 'auth/login.html', {'redirect': redirect})
