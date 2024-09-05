from django import forms
from .models import Vacination

class VacinationForm(forms.ModelForm):
    class Meta:
        model = Vacination
        fields = ['date', 'vacinations']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }