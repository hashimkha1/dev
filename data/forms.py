from django import forms
from django.forms import Textarea
from django.db.models import Q
from .models import Interviews, DSU, JobRole, Interview_Questions
from accounts.models import CustomerUser
class InterviewForm(forms.ModelForm):
    '''========== Performance ============='''
    tableau = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    alteryx = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    sql = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    python = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    '''========== Testing ============='''
    project = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    test_types = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    process = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    '''========== Introduction ============='''
    domain_industry = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    role = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    system_security = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    project_management = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    data_tools = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    communication = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    '''========== SDLC ============='''
    initiation = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    planning = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    design = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    development = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    testing = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    deployment = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    maintenance = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    '''========== Project Story ============='''
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    deliverables = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    challenges = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    solutions = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    '''========== resume ============='''
    summary = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    skills = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    responsibilities = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    '''========== methodology ============='''
    projects = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    releases = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    sprints = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    stories = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
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

class InterviewQuestionsForm(forms.ModelForm):
    class Meta:
        model = Interview_Questions
        fields =['question', 'score','doc','comment','is_active']
        # fields =['category','question_type','client','doc','link']
        labels={
               # 'first_name':'First Name',
                'question':'Question',
                'score':'Score',
                'doc':'Assignment',
                'comment':'Comment',
                'is_active':'Is_active',
                }


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
'''
class UploadForm(forms.ModelForm):
    class Meta:
        model = DocUpload
        fields = ['id','doc_type','doc_name','doc','link']
        labels={
                'doc_type':'Document Type',
                'doc_name':'Document Name',
                'doc':'Document',
        }
'''

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
        
'''
    def __init__(self, **kwargs):
        super(DSUForm, self).__init__(**kwargs)
        self.fields["trained_by"].queryset = CustomerUser.objects.filter(
            # Q(is_admin=True) | Q(is_employee=True)| Q(is_client=True)
            Q(is_client=True)
        )
'''
