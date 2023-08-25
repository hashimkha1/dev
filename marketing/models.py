# from django.db import models

# # Create your models here.
# class Advertisement(models.Model):
#     # Twitter   
#     twitter_api_key = models.CharField(max_length=500, null=True, blank=True)
#     twitter_api_key_secret = models.CharField(max_length=500, null=True, blank=True)
#     twitter_bearer_token = models.CharField(max_length=500, null=True, blank=True)
#     twitter_access_token = models.CharField(max_length=500, null=True, blank=True)
#     twitter_access_token_secret = models.CharField(
#         max_length=500, null=True, blank=True
#     )
#     # Facebook
#     facebook_access_token = models.CharField(max_length=500, null=True, blank=True)
#     facebook_page_id = models.CharField(max_length=100, null=True, blank=True)
#     page_name = models.CharField(max_length=100, null=True, blank=True)
#     post_description = models.TextField(null=True, blank=True)
#     image = models.ImageField(upload_to="Uploads/Facebook/", null=True, blank=True)
#     author= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # whatsapp
#     whatapp_group_name = models.CharField(max_length=100, null=True, blank=True)
#     whatapp_group_id = models.CharField(max_length=100, null=True, blank=True)
#     whatapp_image_url = models.CharField(max_length=500, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # updated_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.post_description
    
# class Whatsapp(models.Model):
#     # whatsapp
#     product_id = models.CharField(max_length=100, null=True, blank=True)
#     token = models.CharField(max_length=100, null=True, blank=True)
#     screen_id = models.CharField(max_length=500, null=True, blank=True)
#     group_name = models.CharField(max_length=100, null=True, blank=True)
#     group_id = models.CharField(max_length=100, null=True, blank=True)
#     image_url = models.CharField(max_length=500, null=True, blank=True)
#     message= models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.group_name