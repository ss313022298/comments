from django import forms


class PoisForms(forms.Form):
    poi_title = forms.CharField(max_length=20, required=True)
    poi_content = forms.CharField(max_length=1000, required=True)
