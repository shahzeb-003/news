from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'date_of_birth', 'profile_image', 'favorite_categories',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['favorite_categories'].required = True

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'date_of_birth', 'profile_image', 'favorite_categories']

    def save(self, commit=True):
        # First save the main object (but don't commit if requested)
        user = super().save(commit=False)

        if commit:
            user.save()
            # If 'commit' is True, save many-to-many data for the form.
            self.save_m2m()

        return user
