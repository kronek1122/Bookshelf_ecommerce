from django import forms
from django.contrib.auth.models import User
from .models import Messages


class UserDataChangeForm(forms.ModelForm):
    email = forms.EmailField(required=False, label='New email')
    first_name = forms.CharField(max_length=30, required=False, label ='New first name')
    last_name = forms.CharField(max_length=30, required=False, label='New last name')

    class Meta:
        model = User
        fields = [ 'email', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.user = user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            existing_user = User.objects.filter(email=email).exclude(pk=self.user.pk).first()

            if existing_user:
                raise forms.ValidationError('This email address is already in use.')

        return email

    def save(self, commit=True):
        if self.user:
            if self.cleaned_data['email']:
                self.user.email = self.cleaned_data['email']
            if self.cleaned_data['first_name']:
                self.user.first_name = self.cleaned_data['first_name']
            if self.cleaned_data['last_name']:
                self.user.last_name = self.cleaned_data['last_name']

            if commit:
                self.user.save()

        return self.user

class UsernameChangeForm(forms.ModelForm):
    username = forms.CharField(max_length=30, label='New username')

    class Meta:
        model = User
        fields = [ 'username']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.user = user

    def clean_username(self):
        username = self.cleaned_data.get('username')
        existing_user = User.objects.filter(username=username).exclude(pk=self.user.pk).first()
        if existing_user:
            raise forms.ValidationError('This username is already in use.')

        return username

    def save(self, commit=True):
        if self.user:
            self.user.username = self.cleaned_data['username']

            if commit:
                self.user.save()

        return self.user


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = [
            'sender',
            'receiver',
            'message'
        ]