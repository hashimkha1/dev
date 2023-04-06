from django import forms
from django.db.models import Q
from django.forms import ModelForm, Textarea
from .models import Post,Testimonials
from django.contrib.auth import get_user_model
# User=settings.AUTH_USER_MODEL
User = get_user_model()

class PostForm(forms.ModelForm):
    class Meta:  
        model = Testimonials  
        # fields = ['writer', 'title', 'content']
        fields = ['title', 'content']
        widgets = {"content": Textarea(attrs={"cols": 40, "rows": 3})}

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
        # filter author queryset based on user type
        # self.fields['writer'].queryset = User.objects.filter(Q(is_client=True))# | Q(is_employee=True))