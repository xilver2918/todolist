from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    #ModelForm 상속해서 입력양식 만들게요 

    class Meta:
        model = Todo #todo 기준으로 작동 
        fields = ["title"] #사용자에게 title을 입력받겠다. 