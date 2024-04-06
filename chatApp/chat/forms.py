from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
        labels = {
          'first_name': 'First name',
          'last_name': 'Last name',
          'username': 'Username',
          'email': 'E-Mail',
          'password': 'Password'
        }
        error_messages = {
          'username': {
            'required': 'Username cannot be empty',
            'unique': 'This username already exists'
          },
          'email': {
            'unique': 'This Email already exists',
            'invalid': 'Invalid E-mail'
          },
          'password': {
            'required': 'Field cannot be empty'
          }
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")
            
        return cleaned_data