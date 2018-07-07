from django import forms


class TagsForms(forms.Form):
    tag_name = forms.CharField(max_length=100)
