from django.db import models


# Create your models here.
class Prof(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(null=True)
    created = models.DateTimeField(auto_now_add=True)
