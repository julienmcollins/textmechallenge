from django.db import models

# Create your models here.
"""
class URLObject(models.Model):
    url = models.ForeignKey(URLObject, on_delete=models.CASCADE)
    url_text = models.CharField(max_length=256)
    def __str__(self):
        return self.url_text
"""
class Url(models.Model):
    url = models.CharField(max_length=256)
    short = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.url
