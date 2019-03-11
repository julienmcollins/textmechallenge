from django import forms
from .models import Url

class UrlForm(forms.ModelForm):
    url = forms.CharField(required=False)
    short = forms.CharField(required=False)
    class Meta:
        model = Url
        fields = ['url', 'short']
