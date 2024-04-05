from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .forms import RegistrationForm
from .utils import *

@login_required(login_url='/login/') #redirect when user is not logged in
def index(request):
  if request.method == 'POST':
    print("Received data " + request.POST["messageField"])
    myChat, created = Chat.objects.get_or_create(id=1)
    new_message = Message.objects.create(text=request.POST["messageField"], chat=myChat, author=request.user, receiver=request.user)
    serialized_obj = serializers.serialize('json', [ new_message, ])
    return JsonResponse(serialized_obj[1:-1], safe=False)
  chatMessages = Message.objects.filter(chat__id=1)
  return render(request, 'chat/index.html', {'messages': chatMessages})


def login_view(request):
  redirect = request.GET.get('next', '/chat/')
  if request.method == 'POST':
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user:
      login(request, user)
      return HttpResponseRedirect(request.POST.get('redirect'))
    else:
      return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
  return render(request, 'auth/login.html', {'redirect': redirect})


def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/login/')



def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.save()
      
      authenticated_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
      )
        
      if authenticated_user:
        login(request, authenticated_user)
        return redirect('/chat/')
  else:
    form = RegistrationForm()
  return render(request, 'auth/register.html', {'form': form})
