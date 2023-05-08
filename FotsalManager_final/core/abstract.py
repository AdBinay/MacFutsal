from django.db import models
from .utility import time_ago

class CreateUpdatedModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def created_since(self):return time_ago(self.created_at)
    def updated_since(self):return time_ago(self.updated_at)

    class Meta:
        abstract = True
