from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=64, unique=True)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=64)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
