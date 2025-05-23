from django import forms
from goods.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'rating')
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите свой комментарий...'
            }),
            'rating': forms.HiddenInput()
        }
        labels = {
            'text': 'Ваш комментарий',
        }
