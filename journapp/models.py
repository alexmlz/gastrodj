from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Journal(models.Model):
    content = models.TextField()
    cre_date = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=50)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False
    )
    # categroy can be more than one which means need an own model
