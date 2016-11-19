from django import forms

class ComponentForm(forms.Form):
    index=forms.IntegerField()
    file=forms.FileField (
        label="Select a file",
        help_text="max. 43 MB"
    )