from django.db import models
#authentication 
from authentication.models import User

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):  
        return f"Admin {self.user.first_name} {self.user.last_name}"