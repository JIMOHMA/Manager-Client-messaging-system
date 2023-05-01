from django.db import models

# Create your models here.
class Message(models.Model):
  userName          = models.CharField(max_length=255)
  message           = models.CharField(max_length=255)
  messageTimeStamp  = models.TimeField(auto_now_add=False, blank=True)