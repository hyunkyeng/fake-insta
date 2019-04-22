from django import forms
from .models import Post, Image, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content',]
        
class ImageForm(forms.ModelForm):
    file = forms.ImageField(widget=forms.FileInput(attrs={'multiple':True,}))
    class Meta:
        model = Image
        fields = ['file',]
        # widgets = {
        #     'file': forms.FileInput(attrs={'multiple':True}),
        # }
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(label="댓글  ",)
    class Meta:
        model = Comment
        fields = ['content',]