from django import forms
from .models import Post, ContentBlock
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'BlogCover', 'intro', 'category']
        widgets = {
            'intro': forms.Textarea(attrs={
                'cols': 30,  # Width of the textarea
                'rows': 5,  # Height of the textarea
            }),
            # You can customize other fields as needed
        }

class ContentBlockForm(forms.ModelForm):
    class Meta:
        model = ContentBlock
        fields = ['block_type', 'content', 'image', 'caption', 'order']
        widgets = {
            'content': forms.Textarea(attrs={
                'cols': 30,  # Width of the textarea
                'rows': 5,  # Height of the textarea
            }),
            # You can customize other fields as needed
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Add a comment...',
                'rows': 2,
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Post Comment', css_class='btn btn-primary btn-block'))