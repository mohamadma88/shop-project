from wsgiref.validate import validator
from django import forms
from account.models import Address


class CreateAddress(forms.ModelForm):
    user = forms.IntegerField(required=False)

    class Meta:
        model = Address
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            '__all__': forms.TextInput(attrs={'class':'control-group'})
        }

class LoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'phone number'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'password'}))


class RegisterForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'phone number'}))


class CheckOtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'phone number'}))
