from datetime import datetime
from tkinter import Widget
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Korisnici, Dokumenti, Korisnici, Student_Dokument

User = get_user_model()

##LOGIN FORM
class LoginForm(forms.Form):
    Email    = forms.EmailField(label='Email')
    Password = forms.CharField(widget=forms.PasswordInput)

##REGISTER FORM
class RegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('Email','Role')

    def check_password(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
        return user



##CREATE USER
class UserCreate(forms.ModelForm):
    class Meta:
        model = Korisnici
        exclude = ('last_login',)
        fields = '__all__'

##ADD DOCUMENT

class DocumentCreate(forms.ModelForm):
    class Meta:
        model = Dokumenti
        fields= ('Naslov', 'Dokument',)
        
##SHARE TO STUDENT

class ShareForm(forms.ModelForm):
    class Meta:
        model = Student_Dokument
        fields = ('Studenti',)
        exclude = ('DokumentID_id',)
        
        
    Studenti = forms.ModelMultipleChoiceField(queryset=Korisnici.objects.filter(Role_id=3),widget=forms.CheckboxSelectMultiple)
    
