from django import forms
from django.db.models import Q
from django.forms import ModelForm, Textarea
from .models import Rated,Post,Testimonials
from django.contrib.auth import get_user_model
# User=settings.AUTH_USER_MODEL
User = get_user_model()

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rated
        fields = ['first_name','last_name','topic', 'punctuality','communication','understanding']
        labels={
                'first_name':'First Name',
                'last_name':'Last Name',
                'topic':'Topic',
                'punctuality':'Punctuality',
                'communication':'Communication',
                'understanding':'Understanding',

        }
        
    def __init__(self, *args, **kwargs):
        super(RatingForm,self).__init__(*args, **kwargs)
        self.fields['punctuality'].empty_label= "Select"
        self.fields['communication'].empty_label= "Select"
        self.fields['understanding'].empty_label= "Select"
        self.fields['topic'].required= False

# from django import forms
# from django.contrib.auth.models import User
# from .models import Post

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


# class PostForm(forms.ModelForm):  
#     class Meta:  
#         model = Post  
#         fields=['author','title','content']
#         widgets = {"content": Textarea(attrs={"cols": 40, "rows": 3})}

#     def __init__(self, *args, **kwargs):
#         super(PostForm, self).__init__(*args, **kwargs)
#         # self.fields["title"].empty_label = "Select"