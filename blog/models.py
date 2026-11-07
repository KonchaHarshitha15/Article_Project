from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.urls import reverse

class post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics',default='https://1drv.ms/u/c/151b0fd346ee85e0/IQBZIHjq4Q19R4swudJ5IBthAcAHEr3h-abW29tNDvy6jQA?e=sInRuq')