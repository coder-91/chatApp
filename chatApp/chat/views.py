from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core import serializers
from .utils import *

@login_required(login_url='/login/') #redirect when user is not logged in
def index(request):
  """_summary_

  Args:
      request (_type_): _description_

  Returns:
      _type_: _description_
  """
  if request.method == 'POST':
    print("Received data " + request.POST["messageField"])
    myChat = Chat.objects.get(id=1)
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
      # Wenn die URL so aussieht: http://example.com/some-path/?next=/redirect-here/, dann würde request.GET.get('next') den Wert '/redirect-here/' zurückgeben.
      return HttpResponseRedirect(request.POST.get('redirect'))
    else:
      return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
  return render(request, 'auth/login.html', {'redirect': redirect})

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/login/')

def register(request):
  form_data = {}
  error_messages = {}
  
  if request.method == 'POST':
    form_data['firstName'] = request.POST.get('firstName', '')
    form_data['lastName'] = request.POST.get('lastName', '')
    form_data['username'] = request.POST.get('username', '')
    form_data['email'] = request.POST.get('email', '')
    form_data['password'] = request.POST.get('password', '')
    form_data['confirmPassword'] = request.POST.get('confirmPassword', '')
    
    error_messages['firstName'] = None
    error_messages['lastName'] = None
    error_messages['username'] = None
    error_messages['email_invalid'] = None
    error_messages['email_exists'] = None
    error_messages['confirmPassword'] = None
    
    # Überprüfung, ob der Vorname nicht leer ist
    if form_data['firstName'].strip() == '':
      error_messages['firstName'] = 'Vorname darf nicht leer sein'
      
    # Überprüfung, ob der Nachname nicht leer ist
    if form_data['lastName'].strip() == '':
      error_messages['lastName'] = 'Nachname darf nicht leer sein'
    
    # Überprüfung, ob der Benutzername in der Datenbank existiert
    if User.objects.filter(username__iexact = form_data['username']).exists():
      error_messages['username'] = 'Dieser Benutzername existiert bereits'
    
    # Überprüfung, ob die E-Mail gültig ist
    if validate_email(form_data['email']):
      error_messages['email_invalid'] = 'Invalid E-mail'
      
    # Überprüfung, ob die E-Mail in der Datenbank existiert
    if User.objects.filter(email__iexact=form_data['email']).exists():
      error_messages['email_exists'] = 'Diese E-Mail existiert bereits'

    # Überprüfung, ob die Passwörter übereinstimmen
    if form_data['password'] != form_data['confirmPassword']:
      error_messages['confirmPassword'] = 'Passwörter stimmen nicht überein'
    
    # Überprüfung, ob keine Validierungsfehler vorliegen
    if all(value == None for value in error_messages.values()):
        # Keine Validierungsfehler, Benutzer erstellen und authentifizieren
        user = User.objects.create_user(
            first_name=form_data['firstName'],
            last_name=form_data['lastName'],
            username=form_data['username'],
            email=form_data['email'],
            password=form_data['password']
        )
        
        authenticated_user = authenticate(
            username=form_data['username'],
            password=form_data['password']
        )
        
        if authenticated_user:
          login(request, authenticated_user)
          return HttpResponseRedirect('/chat/')
  return render(request, 'auth/register.html', {'form_data': form_data, 'error_messages': error_messages})
