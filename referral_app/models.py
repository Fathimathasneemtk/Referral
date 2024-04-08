from django.db import models
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    referral_code = models.CharField(max_length=100, blank=True, null=True)
    points = models.IntegerField(default=0)  # Add points field for tracking user points
    timestamp = models.DateTimeField(auto_now_add=True)