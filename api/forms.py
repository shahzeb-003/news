from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'date_of_birth', 'profile_image', 'favorite_category',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['favorite_category'].required = True

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'date_of_birth', 'profile_image', 'favorite_category']
