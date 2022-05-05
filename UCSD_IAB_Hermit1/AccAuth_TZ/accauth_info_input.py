
from django.contrib.auth.models import User
from django import forms

class AccAuth_Info_Input(forms.Form):
   	i_user = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label = "User")
   	i_pass = forms.CharField(widget = forms.PasswordInput(),
                             label  = "Password")
   