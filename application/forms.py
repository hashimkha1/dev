from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (
    UserProfile,
    Application,
    # InteviewUploads,
    # Policy,
    Rated,
    Reporting,
)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'section',
            'account_number',
            'account_holder_name',
            'bank_name',
            'administration_letter',
            'handwritten_letter',
            'academic_credentials',   
        ]
        labels ={
            'account_number': 'Account number',
            'account_holder_name': 'Account Holder Name',
            'bank_name': 'Bank Name',
            'administration_letter': 'Administration Letter',
            'handwritten_letter': 'Handwritten Letter',
            'academic_credentials': 'Academic Credentials',
        }
# class ApplicantProfileFormA(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         # fields = ["section", "upload_a"]
#         fields = ["section"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
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
            # 'account_number ',
            # 'account_holder_name',
            # 'bank_name',
            # 'administration_letter',
            # 'handwritten_letter',
            # 'academic_credentials',
        ]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "username": "User Name",
            "email": "Email",
            "gender": "gender",
            "type": "type",
            # 'account_number': 'Account number',
            # 'account_holder_name': 'Account Holder Name',
            # 'bank_name': 'Bank Name',
            # 'administration_letter': 'Administration Letter',
            # 'handwritten_letter': 'Handwritten Letter',
            # 'academic_credentials': 'Academic Credentials',
        }

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.fields["type"].empty_label = "Select"

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rated
        fields = [
            "employeename",
            "rating_date",
            "type",
            "topic",
            "data_tools",
            "uploadlinkurl",
            "projectDescription",
            "requirementsAnalysis",
            "development",
            "testing",
            "deployment",
            "totalpoints"
        ]
        labels = {
            "employeename":"Employee Name",
            "rating_date": "Date",
            "type": "type",
            "topic": "Topic",
            "data_tools": "Data Tools",
            "uploadlinkurl": "Upload link url",
            "projectDescription": "Project Description",
            "requirementsAnalysis": "Requirements Analysis",
            "development": "Development",
            "testing": "Testing",
            "deployment": "Deployment"
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RatingForm, self).__init__(*args, **kwargs)
        self.fields["topic"].required = False
        self.fields["type"].required = False
        self.fields["rating_date"].required = False
        if self.request and self.request.user:
            is_employee = self.request.user.is_staff
            if is_employee:
                self.fields["uploadlinkurl"].required = False
            else:
                self.fields["uploadlinkurl"].required = True
        else:
            # handle the case when self.request is None or self.request.user is None
            self.fields["uploadlinkurl"].required = True


# class InterviewForm(forms.ModelForm):
#     class Meta:
#         model = InteviewUploads
#         fields = ["username", "ppt", "report", "workflow", "proc", "other"]
#         labels = {
#             "ppt": "Powerpoint",
#             "report": "Tableau Reports",
#             "workflow": "Alteryx Workflow",
#             "proc": "SQL Script",
#             "other": "Other Documents",
#         }


class ReportingForm(forms.ModelForm):
    class Meta:
        model = Reporting
        fields = [
            "reporter",
            "name",
            "rate",
            "reporting_date",
            "method",
            "interview_type",
            "link",
            "comment",
        ]
        labels = {
            "reporter": "User Name",
            "name": "Dev Name",
            "rate": "Rate Per Hour",
            "method": "Method",
            "interview_type": "Interview Type",
            "reporting_date": "Reporting Date(mm/dd/yy)",
            "link": "Link",
            "comment": "Comment",
        }
