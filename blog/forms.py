from django import forms
from .models import Post, Comment



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['user', 'title', 'description', 'content', 'img', "slug"]



class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={
                                'class':'form-control w-100',
                                'id':'comment',
                                'name':'comment',
                                'cols':'30',
                                'rows':'9',
                                'placeholder':'Write Comment'}))
