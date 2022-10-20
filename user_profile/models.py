from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Profile(models.Model):
    user_fk = models.OneToOneField(to=User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=17, blank=True, null=True, help_text='Contact phone number')
    user_type = models.IntegerField(blank=True, null=True, default=3, help_text='1. Admin, 2. Editor, 3. Customer' )

    slug = models.CharField(max_length=15, blank=True, null=True)

    
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_send_time = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return self.slug

    def save(self , *args, **kwargs):
        if self.slug:
            super(Profile, self).save(*args, **kwargs)
        else:
            self.slug = slugify(self.user_fk.username)
            super(Profile, self).save(*args, **kwargs)
