from django import forms

class DocumentForm(forms.Form):
    file=forms.FileField (
        label="Select a file",
        help_text="max. 43 MB"
    )
