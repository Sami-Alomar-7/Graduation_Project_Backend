from django.db import models

#authentication 
from authentication.models import *

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Customer {self.user.username}"