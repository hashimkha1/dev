from django.contrib import admin
from .models import Post,Rate,Rated

# Register your models here.
admin.site.register(Post)
admin.site.register(Rate)
admin.site.register(Rated)