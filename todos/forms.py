from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "due_date"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "todo-dialog-input",
                    "autocomplete": "off",
                }
            ),
            "due_date": forms.DateInput(
                attrs={
                    "class": "todo-dialog-input todo-dialog-date",
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
        }