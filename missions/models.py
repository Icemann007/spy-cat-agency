from django.db import models

from cats.models import Cat


class Mission(models.Model):
    cat = models.ForeignKey(
        Cat, on_delete=models.SET_NULL, related_name="missions", null=True, blank=True
    )
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        cat_name = self.cat.name if self.cat else "Unassigned"
        return f"Mission {self.pk} ({cat_name})"


class Target(models.Model):
    name = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    notes = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)
    mission = models.ForeignKey(
        Mission, related_name="targets", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} ({self.country})"
