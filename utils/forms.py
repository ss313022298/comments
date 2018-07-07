# encoding:utf-8
'''
Created on 2015年12月21日

@author: hanlucen
'''
from django.forms.fields import Field
from django.utils.translation import ugettext_lazy
from django.core import validators
from django.core.exceptions import ValidationError
import json
from django import forms


def validate_form(form_class, data):
    form = form_class(data)
    if form.is_valid():
        return True, form.cleaned_data
    errors = []
    for key, field in form.declared_fields.items():
        if field.required and key not in data:
            errors.append({"field": key, "code": "missing_field"})
        elif key in form.errors:
            errors.append({"field": key, "code": "invalid"})
    return False, errors


class SimpleDictField(Field):
    default_error_messages = {
        'invalid': ugettext_lazy('Enter a valid value.'),
    }

    def __init__(self, inner_field=None, *args, **kwargs):
        self.inner_field = inner_field
        super(SimpleDictField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if type(value) is str:
            try:
                value = json.loads(value)
            except ValueError:
                pass
        if type(value) is not dict:
            raise ValidationError(self.error_messages['invalid'])
        return value


class NullBooleanField(Field):
    values = {
        '0': False,
        '1': True,
        'true': True,
        'false': False,
        'True': True,
        'False': False
    }

    def clean(self, value):
        super(NullBooleanField, self).clean(value)

        if not self.required:
            if value in [None, '']:
                return None

        value = str(value).lower()
        if value not in self.values:
            raise ValidationError('', code='type_invalid')

        return self.values[value]


class PagesPageNumForm(forms.Form):
    page_num = forms.IntegerField(min_value=1, required=True)
    page_size = forms.IntegerField(max_value=50, required=True)

    def clean_page_num(self):
        page_num = self.cleaned_data['page_num']
        return page_num if page_num else 1

    def clean_page_size(self):
        page_size = self.cleaned_data['page_size']
        return page_size if page_size else 50


class ReviewGetForm(PagesPageNumForm):
    reviewed_status = forms.IntegerField(max_value=50, required=False)


class ReviewForm(forms.Form):
    remarks = forms.CharField(max_length=250, required=False)
    authorize_code = forms.IntegerField(min_value=1, max_value=2, required=True)

    def clean_authorize_code(self):
        field = self.cleaned_data['authorize_code']
        if field == 1:
            field = 2
        else:
            field = 3
        return field
