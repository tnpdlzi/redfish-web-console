from django.db import models

class Instance(models.Model):
    name = models.CharField(max_length=70, blank=True, default='')
    ip = models.CharField(max_length=200, blank=True, default='')
    os = models.CharField(max_length=50, blank=True, default='')
    iType = models.CharField(max_length=50, blank=True, default='')
    keyPair = models.CharField(max_length=100, blank=True, default='')
    area = models.CharField(max_length=50, blank=False, default='')
    status = models.CharField(max_length=10)