from django import forms


class CommentsForms(forms.Form):
    content = forms.CharField(max_length=200, required=True)
    tag = forms.CharField(max_length=200, required=True)


class ReplyForms(forms.Form):
    content = forms.CharField(max_length=200, required=True)
