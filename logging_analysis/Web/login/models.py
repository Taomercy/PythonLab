from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=128, unique=True)
    full_name = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user_id
    
    class Meta:
        ordering = ['create_at']
