from .models import AutomobilisReview
from .models import Profilis
from django import forms
from django.contrib.auth.models import User

class AutomobilisReviewForm(forms.ModelForm):
    class Meta:
        model = AutomobilisReview
        fields = ('content', 'automobilis', 'reviewer',)
        widgets = {'automobilis': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']