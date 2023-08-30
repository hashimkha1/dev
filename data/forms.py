from django import forms
from django.forms import Textarea
from django.db.models import Q
from .models import Interviews, DSU, JobRole, Training_Responses,Prep_Questions
from accounts.models import CustomerUser
class InterviewForm(forms.ModelForm):
    '''========== Performance ============='''
    tableau = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    alteryx = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    sql = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    python = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    '''========== Testing ============='''
    project = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    test_types = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    process = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    '''========== Introduction ============='''
    domain_industry = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}),label='Domain/Industry',required=False,min_length=150)
    role = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    system_security = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    project_management = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    data_tools = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    communication = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    '''========== SDLC ============='''
    initiation = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    planning = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    design = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    development = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    testing = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    deployment = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    maintenance = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    '''========== Project Story ============='''
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    deliverables = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    challenges = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    solutions = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    '''========== resume ============='''
    summary = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    skills = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    responsibilities = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    '''========== methodology ============='''
    projects = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    releases = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    sprints = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    stories = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,min_length=150)
    class Meta:
        model = Interviews
        fields = ['category', 'question_type', 'doc', 'link', 'comment', 'tableau', 'alteryx',
             'sql', 'python','project','test_types','process',"domain_industry", "role",
               "system_security", "project_management", "data_tools", "communication",
               "initiation", "planning", "design", "development", "testing", "deployment", "maintenance",
               "description", "deliverables", "challenges", "solutions","summary","skills","responsibilities",
               "projects", "releases", "sprints", "stories"]
        # fields =['category','question_type','client','doc','link']
        labels={
               # 'first_name':'First Name',
                'client':'username', 
                'category':'Select Job Category',
                'question_type':'Interview Question/topic',
                'doc':'Upload assignment',
                'link':'Paste Your link',
                'comment':'Questions/comments on this section?',
                'tableau':'Tableau on this section',
                'alteryx':'Alteryx on this section',
                'sql':'SQL on this section',
                'python':'Python on this section',
                'domain_industry' : 'Domain/Industry',
               
                }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(InterviewForm, self).__init__(*args, **kwargs)
        self.fields['question_type'].required = False


class PrepQuestionsForm(forms.ModelForm):
    class Meta:
        model = Prep_Questions
        fields = ["questioner","company",'position', 'category',"question", "response","is_answered"]
        labels={
                'questioner':'Client/User', 
                'company':'company', 
                'position':'Position/Role',
                'category':'Topic i.e Methodology,Intro..',
                'question':'question',
                'response':'response',
                }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(PrepQuestionsForm, self).__init__(*args, **kwargs)
        self.fields['question'].required = False

class TrainingResponseForm(forms.ModelForm):
    class Meta:
        model = Training_Responses
        fields =['question', 'score','doc','comment','is_active']
        # fields =['category','question_type','client','doc','link']
        labels={
               # 'first_name':'First Name',
                'question':'',
                'question1':'Your response',
                'doc':'Assignment',
                'comment':'',
                'is_active':'Is_active',
                }
        widgets = {"comment": Textarea(attrs={"cols": 175, "rows": 3})}

class RoleForm(forms.ModelForm):
    class Meta:
        model = JobRole
        fields =['category','question_type','doc','videolink','doclink','desc1','desc2']
        labels={
                    # 'user':'username', 
                    'category':'Category',
                    'question_type':'Question',
                    'doc':'Assignment',
                    'doclink':'PPT/Doc Link',
                    'videolink':'Video Link',
                    'desc1':'Overall Description',
                    'desc2':'Question description',
                }
        widgets = {
                    "desc1": Textarea(attrs={"cols": 30, "rows": 6}),
                    "desc2": Textarea(attrs={"cols": 30, "rows": 6})
                  }
        # widgets = {"desc2": Textarea(attrs={"cols": 15, "rows": 2})}

class DSUForm(forms.ModelForm):
    class Meta:
        model = DSU
        #fields =['client','category','question_type','doc','link']
        fields=['cohort','trained_by','client_name','type','category','task','plan','challenge','uploaded']
        labels={
                'cohort':'Cohort',
                'type':'Client/Staff?',
                'trained_by':'Client Name',
                'client_name':'Trainer', 
                'category':'Category',
                'task':'What Did You Work On?',
                'plan':'What is your next plan of action?',
                'challenge':'What Challenges are you facing?',
                'uploaded' : 'Have you uploaded your assignments to Interview Portal?'
                }