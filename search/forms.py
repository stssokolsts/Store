from django import forms
from models import SearchTerm

class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchTerm
 
    include = ('q',)