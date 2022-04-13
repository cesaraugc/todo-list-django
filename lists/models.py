from django.db import models
from django.conf import settings


class List(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)

class Item(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    # father_item = models.ForeignKey('self', on_delete=models.DO_NOTHING)