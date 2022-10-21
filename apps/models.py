from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class App(models.Model):
    appname=models.CharField(max_length=240)
    appurl=models.CharField(max_length=240)
    user=models.ForeignKey(to=User, on_delete=models.CASCADE)
    
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.appname