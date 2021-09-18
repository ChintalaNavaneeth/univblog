from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Userotp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_st = models.DateTimeField(auto_now=True)
    otp = models.PositiveIntegerField()


class profile(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    fname = models.CharField(null=True, max_length=15, blank=True)
    lname = models.CharField(null=True, max_length=15, blank=True)
    profileimg = models.ImageField(
        null=True, blank=True, default="user.png")
    age = models.DecimalField(null=True, max_digits=2,
                              decimal_places=0, blank=True)
    profession = models.CharField(null=True, max_length=25, blank=True)
    specialization = models.CharField(null=True, max_length=50, blank=True)
    country = models.CharField(null=True, max_length=25, blank=True)
    city = models.CharField(null=True, max_length=25, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
