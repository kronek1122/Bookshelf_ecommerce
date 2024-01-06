from django import forms
from django.contrib.auth.models import User

class AddToShelfForm(forms.Form):
    pass


class UserDataChangeForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = [ 'email', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
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

