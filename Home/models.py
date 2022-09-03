from django.db import models

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=100)
    otp = models.CharField(default='0', max_length=8)
    email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username