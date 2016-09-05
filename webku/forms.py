from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=25)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()

class AddressForm(forms.Form):
    address = forms.CharField()