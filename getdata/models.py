from django.db import models
from datetime import datetime,date
from django.contrib.auth import get_user_model

#User=settings.AUTH_USER_MODEL
User = get_user_model()
# Create your models here.
class CashappMail(models.Model):
	id = models.CharField(max_length=30, unique=True, primary_key=True)
	from_mail = models.CharField(max_length=255)
	to_mail = models.CharField(max_length=255)
	subject = models.CharField(max_length=255)
	file_name = models.CharField(max_length=50)
	full_path = models.CharField(max_length=255)
	text_mail = models.TextField()
	received_date = models.CharField(max_length=255)
	parsed_date = models.DateTimeField(auto_now_add=True)
	amount = models.CharField(max_length=255,blank=True,null=True)
	destination = models.CharField(max_length=255,blank=True,null=True)

	class Meta:
		verbose_name_plural = "Cashapp"

	def __str__(self):
		return self.subject
	
	@property
	def received_date_format(self):
		time_text_date = self.received_date.replace(" ", "").split(",")[-1]
		new_received_date=datetime.strptime(time_text_date,'%d%b%Y%H:%M:%S+0000').date()
		return new_received_date

class ReplyMail(models.Model):
	id = models.CharField(max_length=30, unique=True, primary_key=True)
	from_mail = models.CharField(max_length=255)
	to_mail = models.CharField(max_length=255)
	subject = models.CharField(max_length=255)
	text_mail = models.TextField()
	received_date = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "ReplyMail"

	def __str__(self):
		return self.subject

class Editable(models.Model):
	name = models.CharField(max_length=255,blank=True,null=True)
	putsrow = models.PositiveIntegerField(blank=True,null=True)
	callsrow = models.PositiveIntegerField(blank=True,null=True)

	class Meta:
		verbose_name_plural = "General"

	def __str__(self):
		return self.name

class GotoMeetings(models.Model):
    meeting_topic = models.CharField(max_length=250, null=True, blank=True)
    meeting_id = models.CharField(max_length=100, null=True, blank=True)
    meeting_type = models.CharField(max_length=100, null=True, blank=True)
    recording = models.CharField(max_length=500, null=True, blank=True)
    meeting_start_time = models.CharField(max_length=250, null=True, blank=True)
    meeting_end_time = models.CharField(max_length=250, null=True, blank=True)
    meeting_duration = models.CharField(max_length=100, null=True, blank=True)
    meeting_email = models.CharField(max_length=150, null=True, blank=True)
    attendee_name = models.CharField(max_length=150, null=True, blank=True)
    attendee_email = models.CharField(max_length=150, null=True, blank=True)
    attendee_duration = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    def __str__(self):
        return self.meeting_topic
	
class upwork_Transanctions(models.Model):
    date= models.CharField(max_length=250, null=True, blank=True)
    ref_Id= models.CharField(max_length=250, null=True, blank=True)
    type= models.CharField(max_length=500, null=True, blank=True)
    description= models.CharField(max_length=250, null=True, blank=True)
    agency= models.CharField(max_length=250, null=True, blank=True)
    freelancer= models.CharField(max_length=250, null=True, blank=True)
    team= models.CharField(max_length=250, null=True, blank=True)
    account_name= models.CharField(max_length=250, null=True, blank=True)
    amount= models.CharField(max_length=250, null=True, blank=True)
    balance= models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.ref_Id

class Logs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_in_logs", null=True, blank=True)
    location_in_code = models.CharField(max_length=255, null=True, blank=True)
    reason_code_crash = models.CharField(max_length=255, null=True, blank=True)
    exception = models.CharField(max_length=255, null=True, blank=True)
    api = models.URLField(max_length=255, null=True, blank=True)
    crated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Logs"