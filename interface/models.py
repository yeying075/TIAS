from django.db import models


class Users(models.Model):
    encoding = models.CharField(max_length=30)
    face_done = models.CharField(default='no', max_length=10, null=True)
    text_done = models.CharField(default='no', max_length=10, null=True)


