from django import forms
from django.contrib.auth.models import User


class LoginForms(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)

    password_2 = forms.CharField(label="Parolni takrorlang", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', "first_name", 'email']

        def clean_password2(self):
            data = self.clean_data
            if data['password'] != data['password2']:
                raise forms.ValidationError("Parolingiz bir biriga teng emas")
            return data["password2"]
