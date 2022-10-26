from django.db import models

# Create your models here.

class Violation(models.Model):
    url = models.CharField(max_length=240, blank=True, null=True)
    displayed_url = models.CharField(max_length=240, blank=True, null=True)
    description = models.TextField()
    extra_info = models.CharField(max_length=240, blank=True, null=True)
    position = models.IntegerField()
    title = models.CharField(max_length=240, blank=True, null=True)
    app = models.CharField(max_length=240, blank=True, null=True)
    query = models.CharField(max_length=240, blank=True, null=True)
    violator_url = models.CharField(max_length=240, blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.app