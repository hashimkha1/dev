from django.db import models

class CategoryChoices(models.IntegerChoices):
    Job_Applicant = 1
    Coda_Staff_Member = 2
    Jobsupport = 3
    Student = 4
    investor = 5
    General_User = 6