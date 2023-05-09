from django.db import models
from datetime import datetime

# Create your models here.
class Message(models.Model):
  userName          = models.CharField(max_length=255)
  message           = models.CharField(max_length=255)
  messageTimeStamp  = models.TimeField(default=datetime.now, blank=True) # auto generate time when a message object is created
