from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','phone',]