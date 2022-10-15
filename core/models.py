from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model


# Create your models here.

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    file = models.FileField(upload_to='upload_files')
    filename = models.TextField()
    file_desc = models.TextField()
    file_upTime = models.DateField(default=datetime.now)
    file_ediTime = models.DateField(default=datetime.now)

    def __str__(self):
        return self.user
