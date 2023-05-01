from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User,hospitalShiftDetails

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

# class LoginForm(forms.Form):
#     email = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username','name':'username'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password','name':'password'}))

class NurseRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name','is_nurse']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(NurseRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
  
    

class HospitalRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name','is_hospital']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(HospitalRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class shiftCreationForm(forms.ModelForm):
    class Meta:
        model = hospitalShiftDetails
        fields = ['location', 'date', 'start_time', 'end_time', 'price_per_hour']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'format': 'YYYY-MM-DD'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'format': 'HH:MM'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'format': 'HH:MM'}),
        }


    