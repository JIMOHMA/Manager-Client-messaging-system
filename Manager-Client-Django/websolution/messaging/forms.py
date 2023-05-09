from django import forms

class MessageForm(forms.Form):
    Message = forms.CharField()