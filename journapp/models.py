from django.db import models

# Create your models here.


class Journal(models.Model):
    content = models.TextField()
    cre_date = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=50)
    # categroy can be more than one which means need an own model
