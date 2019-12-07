from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Searches(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    query = models.CharField(max_length=300)
    timestamp= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query


