from django import forms
from .models import AutomobilisReview, User, Profilis, Automobilis

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

class DateInput(forms.DateInput):
    input_type = 'date'

class AutomobilisCreateForm(forms.ModelForm):
    class Meta:
        model = Automobilis
        fields = ['automobilio_modelis', 'due_back']
        widgets = {'reader': forms.HiddenInput(), 'due_back': DateInput()}