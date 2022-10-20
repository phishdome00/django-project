from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class App(models.Model):
    appname=models.CharField(max_length=240)
    appurl=models.CharField(max_length=240)
    user=models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.appname