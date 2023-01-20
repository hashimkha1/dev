from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (
    UserProfile,
    Application,
    InteviewUploads,
    Policy,
    Rated,
    Reporting,
)


class ApplicantProfileFormA(forms.ModelForm):
    class Meta:
        model = UserProfile
        # fields = ["section", "upload_a"]
        fields = ["section"]

    def __init__(self, *args, **kwargs):
        super(ApplicantProfileFormA, self).__init__(*args, **kwargs)
        # self.fields["upload_a"].label = ""


class ApplicantProfileFormB(forms.ModelForm):
    class Meta:
        model = UserProfile
        # fields = ["section", "upload_b"]
        fields = ["section"]

    # def __init__(self, *args, **kwargs):
    #     super(ApplicantProfileFormB, self).__init__(*args, **kwargs)
    #     self.fields["upload_b"].label = ""


class ApplicantProfileFormC(forms.ModelForm):
    class Meta:
        model = UserProfile
        # fields = ["section", "upload_c"]
        fields = ["section"]

    # def __init__(self, *args, **kwargs):
    #     super(ApplicantProfileFormC, self).__init__(*args, **kwargs)
    #     self.fields["upload_c"].label = ""


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
            # "id",
            # "first_name",
            # "last_name",
            "employeename",
            "topic",
            "uploadlinkurl",
            # "punctuality",
            # "communication",
            # "understanding",
            "projectDescription",
            "requirementsAnalysis",
            "development",
            "testing",
            "deployment",
            "totalpoints"

        ]
        labels = {
            # "first_name": "First Name",
            # "last_name": "Last Name",
            "employeename":"Employee Name",
            "topic": "Topic",
            "uploadlinkurl": "Upload link url",
            # "punctuality": "Punctuality",
            # "communication": "Communication",
            # "understanding": "Understanding",
            "projectDescription": "Project Description",
            "requirementsAnalysis": "Requirements Analysis",
            "development": "Development",
            "testing": "Testing",
            "deployment": "Deployment"
        }

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        # self.fields["punctuality"].empty_label = "Select"
        # self.fields["communication"].empty_label = "Select"
        # self.fields["understanding"].empty_label = "Select"
        self.fields["topic"].required = False
        # self.fields["uploadlinkurl"].required = True


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


# class PolicyForm(forms.ModelForm):
#     class Meta:
#         model = Policy
#         fields = ["first_name", "last_name", "policy_type", "description", "policy_doc"]
#         labels = {
#             "first_name": "First Name",
#             "last_name": "Last Name",
#             "policy_type": "Policy Type",
#             "description": "Description",
#             "policy_doc": "Attach Policy",
#         }


class ReportingForm(forms.ModelForm):
    class Meta:
        model = Reporting
        fields = [
            "reporter",
            "rate",
            # "gender",
            "reporting_date",
            "method",
            "interview_type",
            "comment",
        ]
        labels = {
            "reporter": "User Name",
            "rate": "Rate Per Hour",
            # "gender": "Gender",
            "method": "Method",
            "interview_type": "Interview Type",
            "reporting_date": "Reporting Date(mm/dd/yy)",
            "comment": "Comment",
        }
