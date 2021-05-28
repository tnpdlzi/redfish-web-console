from django.db import models

# class Tutorial(models.Model):
#     title = models.CharField(max_length=70, blank=False, default='')
#     description = models.CharField(max_length=200,blank=False, default='')
#     published = models.BooleanField(default=False)
#
#
# class Members(models.Model):
#     idUrl = models.CharField(max_length=70, blank=False, default='')


class Servers(models.Model):
    ip = models.CharField(max_length=100,blank=False, default='')
    username = models.CharField(max_length=100,blank=False, default='')
    password = models.CharField(max_length=100,blank=False, default='')
    grafanaId = models.IntegerField(null=True)
    grafanaUid = models.CharField(max_length=50,blank=False, null=True)
    tempThreshold = models.IntegerField(null=True)
    powerThreshold = models.IntegerField(null=True)
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return [self.id, self.username, self.tempThreshold, self.powerThreshold]

