from django.db import models

# Create your models here.

class Order(models.Model):
    book_id = models.IntegerField()
