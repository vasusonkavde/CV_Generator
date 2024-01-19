from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=30)
    phoneno = models.BigIntegerField()
    email = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    university = models.CharField(max_length=30)
    skills = models.TextField(max_length=100)
    about_you = models.TextField(max_length=100)
    previous_work = models.TextField(max_length=100)
