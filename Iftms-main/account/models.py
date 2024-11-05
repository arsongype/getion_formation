from django.db import models

# Create your models here.
class User(models.Model):
    nom = models.CharField(max_length=128)
    pronom = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username