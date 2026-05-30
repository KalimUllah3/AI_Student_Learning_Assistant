from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document 
        fields = ['title', 'file'] 

class QuestionForm(forms.Form):
    question = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Ask a Question"
    )