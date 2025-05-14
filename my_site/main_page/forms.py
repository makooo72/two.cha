from django import forms
from .models import Comment, Post

class CommentCreationForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('description', )

class PostCreationForm(forms.ModelForm):
    class Meta:
            model = Post
            fields = ('title', 'photo_path', 'description', )
            labels = {
                'title': ('Заголовок'),
                'photo_path': (''),
                'description': ('Описание')
            }