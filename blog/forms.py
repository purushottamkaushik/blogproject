from django import forms
from blog.models import Comment

class EmailForm(forms.Form):
    name = forms.CharField(label="Name",max_length=120)
    sender = forms.CharField(label="From")
    to = forms.EmailField(label="TO")
    message = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name','email','body']


