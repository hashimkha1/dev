from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerUser, Tracker,CredentialCategory,Credential
from django.utils.translation import gettext_lazy as _

# from django.db import transaction

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)
    class Meta:
        model = CustomerUser
        fields = [
            "category",
            "sub_category",
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
            "phone",
            "gender",
            "email",
            "address",
            "city",
            "state",
            "country",
            "resume_file",
            "is_employee",
            "is_applicant",
        ]
        labels = {
            "sub_category": "",
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "gender": "",
            "phone": "",
            "address": "",
            "city": "",
            "state": "",
            "country": "",
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields['category'].required= True
        # set category initial=1 and added category
        self.fields["category"].initial = 1
        self.fields["sub_category"].initial = 1
        self.fields["gender"].required = True
        self.fields["country"].required = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user

#==========================CREDENTIAL FORM================================
class CredentialCategoryForm(forms.ModelForm):  
    class Meta:  
        model = CredentialCategory  
        fields = ['department','category', 'slug','description', 'is_active','is_featured']
        widgets = {
            # Use SelectMultiple below
            "category":forms.SelectMultiple(attrs={'class':'form-control', 'category':'category'}),
            "description": Textarea(attrs={"cols": 40, "rows": 2})
            }

class CredentialForm(forms.ModelForm):  
    class Meta:  
        model = Credential
        fields = ['category','name', 'added_by','slug','user_types','description','password','link_name','link','is_active','is_featured']
        labels={
                'link_name':'username/email',
                'link':'Link/url',
                'user_types':'Specify Who Can Access this Credential?'
        }
        widgets = {
            # Use SelectMultiple below
            "category":forms.SelectMultiple(attrs={'class':'form-control', 'id':'category'}),
            "description": Textarea(attrs={"cols": 40, "rows": 2})
            }

""" 
#==========================APPLICATION FORM-APPLICANTS================================

class ApplicationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomerUser
        fields = ['category','first_name','last_name','username','password1','password2','phone','gender', 'email','address','city','state','country']
        labels={
                'category':'Registering as:',
                'first_name':'First Name',
                'last_name':'Last Name',
                'username':'User Name',
                'email':'Email',
                'gender':'Gender',
                'phone':'Phone',
                'address':'Address',
                'city':'City',
                'state':'State',
                'country':'Country',
                'resume':'resume',
        }

    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        self.fields['category'].empty_label= "Select"

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

"""


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


"""
username_validator = UnicodeUsernameValidator()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: First Name',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: Last Name',
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.',
                             widget=(forms.TextInput(attrs={'class': 'form-control'})))
    phone = forms.CharField(max_length=20, min_length=4, required=True, help_text='Required: Phone Number',
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    password1 = forms.CharField(label=_('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=_('Just Enter the same password, for confirmation'))
    username = forms.CharField(
        label=_('Username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={'unique': _("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','phone', 'email', 'password1', 'password2',)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'email','password1', 'password2']
        labels={
            'first_name':"First Name",
            'last_name':"Last Name",
            'username':"User Name",
        }


class UserLoginForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = CustomerUser
        fields = ['username', 'email']
     """
