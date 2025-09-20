from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    """
    A form for creating a new Petition instance.
    """
    class Meta:
        model = Petition
        fields = ['movie_title']
        widgets = {
            'movie_title': forms.TextInput(attrs={
                # Use Bootstrap's form control classes
                'class': 'form-control bg-dark text-white',
                'placeholder': 'Enter a movie title to petition for...'
            })
        }
        labels = {
            'movie_title': '' # Hide the default label
        }

