from django.forms import ModelForm, TextInput, Textarea
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code']
        widgets = {
           'name': TextInput(attrs={"class":'form-control form-control-lg','placeholder': 'Название виджета'})
        }
