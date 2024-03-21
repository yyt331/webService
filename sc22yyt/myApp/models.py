from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Agency(models.Model):
    agency_name = models.CharField(max_length=100)
    url = models.URLField(unique=True)
    agency_code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.agency_name
        
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Story(models.Model):
    CATEGORIES = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia'),
    ]

    REGIONS = [
        ('uk', 'United Kingdom'),
        ('eu', 'Europe'),
        ('w', 'World'),
    ]

    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=30, choices=CATEGORIES)
    region = models.CharField(max_length=30, choices=REGIONS)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    date = models.DateTimeField(default=timezone.now)
    details = models.CharField(max_length=128)

    def __str__(self):
        return self.headline