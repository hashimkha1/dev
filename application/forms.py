from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (
    Applicant_Profile,
    Application,
    InteviewUploads,
    Policy,
    Rated,
    Reporting,
)


class ApplicantProfileFormA(forms.ModelForm):
    class Meta:
        model = Applicant_Profile
        fields = ["section", "upload_a"]


class ApplicantProfileFormB(forms.ModelForm):
    class Meta:
        model = Applicant_Profile
        fields = ["section", "upload_b"]


class ApplicantProfileFormC(forms.ModelForm):
    class Meta:
        model = Applicant_Profile
        fields = ["section", "upload_c"]


class ApplicantForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Application
        fields = [
            "type",
            "first_name",
            "last_name",
            "gender",
            "username",
            "phone",
            "email",
            "country",
            "resume",
        ]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "username": "User Name",
            "email": "Email",
            "gender": "gender",
            "type": "type",
        }

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.fields["type"].empty_label = "Select"


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rated
        fields = [
            "id",
            "first_name",
            "last_name",
            "topic",
            "punctuality",
            "communication",
            "understanding",
        ]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "topic": "Topic",
            "punctuality": "Punctuality",
            "communication": "Communication",
            "understanding": "Understanding",
        }

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        self.fields["punctuality"].empty_label = "Select"
        self.fields["communication"].empty_label = "Select"
        self.fields["understanding"].empty_label = "Select"
        self.fields["topic"].required = False


class InterviewForm(forms.ModelForm):
    class Meta:
        model = InteviewUploads
        fields = ["username", "ppt", "report", "workflow", "proc", "other"]
        labels = {
            "ppt": "Powerpoint",
            "report": "Tableau Reports",
            "workflow": "Alteryx Workflow",
            "proc": "SQL Script",
            "other": "Other Documents",
        }


"""  
class InterviewForm(forms.ModelForm):
    class Meta:
        model = FirstUpload
        fields = ['username','first_name','last_name','ppt','report','workflow', 'proc']
        labels={
                'username':'User Name',
                'first_name':'First Name',
                'last_name':'Last Name',
                'ppt':'Powerpoint',
                'report':'Tableau Reports',
                'workflow':'Alteryx Workflow',
                'proc':'SQL Script',

                }
"""


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ["first_name", "last_name", "policy_type", "description", "policy_doc"]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "policy_type": "Policy Type",
            "description": "Description",
            "policy_doc": "Attach Policy",
        }


class ReportingForm(forms.ModelForm):
    class Meta:
        model = Reporting
        fields = [
            "first_name",
            "last_name",
            "gender",
            "reporting_date",
            "method",
            "interview_type",
            "comment",
        ]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "gender": "Gender",
            "method": "Method",
            "interview_type": "Interview Type",
            "reporting_date": "Reporting Date(mm/dd/yy)",
            "comment": "Comment",
        }
