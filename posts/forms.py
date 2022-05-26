from django import forms
from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'placeholder': 'Название блюда...'}))
    content = forms.CharField(label='Рецепт', widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Распишите рецепт...'}))
    ingredients = forms.CharField(label='Ингредиенты', widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Молоко - 500мл,\nМука - 200гр,'}))
    image = forms.ImageField(label='Фото', required=False)

    class Meta:
        model = Post
        fields = ('name', 'ingredients', 'content', 'image')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add comment...'}))

    class Meta:
        model = Comment
        fields = ('body',)