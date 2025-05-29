from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Order

class UserRegistration(UserCreationForm):
    first_name = forms.CharField(max_length=80, required=True, widget=forms.TextInput (attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.EmailField(max_length=200, required=True, widget=forms.EmailInput(attrs={'placeholder':'email'}))
    mobile = forms.CharField(max_length=15, required=True,widget=forms.TextInput(attrs={'placeholder':'your number'}))
    agree_term = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class':'term-checkbox'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','email','mobile','agree_term','password1','password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            UserProfile.objects.create(
            user=user,
            mobile=self.cleaned_data['mobile']
        )
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=200, required=True,widget=forms.TextInput(attrs={'placeholder':'enter your email'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder':'enter your password'}))
    remember_me = forms.BooleanField(required=False,widget=forms.CheckboxInput())

# form for checkout
NEPAL_PROVINCES = [
    ('Koshi', 'Koshi'),
    ('Madhesh', 'Madhesh'),
    ('Bagmati', 'Bagmati'),
    ('Gandaki', 'Gandaki'),
    ('Lumbini', 'Lumbini'),
    ('Karnali', 'Karnali'),
    ('Sudurpashchim', 'Sudurpashchim'),
]
class OrderForm(forms.ModelForm):
    state = forms.ChoiceField(choices=NEPAL_PROVINCES, required=True)
    class Meta:
        model = Order
        fields = [
            'firstName','lastName','country','city','state','zipCode',
            'phone','email'

        ]
        


