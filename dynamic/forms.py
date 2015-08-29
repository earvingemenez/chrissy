from django import forms


class CreateTableForm(forms.Form):

    model_name = forms.CharField()
    fields = forms.CharField()