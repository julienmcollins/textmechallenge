from django import forms
from .models import Url, UrlChoice

class UrlFormChoice(forms.ModelForm):
    url = forms.BooleanField(required=False)
    short = forms.BooleanField(required=False)
    class Meta:
        model = UrlChoice
        fields = ['url', 'short']

class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ['url']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ['short']
