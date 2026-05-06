from django import forms
from CalorieCounter.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# user creation form
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# authentication form
class LoginForm(AuthenticationForm):
    pass

# profile form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = BasicInfoModel
        fields = '__all__'
        exclude = ['user', 'bmr']

# calorie form
class ConsumedCalorieForm(forms.ModelForm):
    class Meta:
        model = ConsumedCalories
        fields = '__all__'
        exclude = ['consumed_by']