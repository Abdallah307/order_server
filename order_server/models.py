from django.db import models

# Create your models here.

class Order(models.Model):
    book_id = models.IntegerField()


    def __str__(self):
        return f"Order ID : {self.id} | book ID : {self.book_id}"
