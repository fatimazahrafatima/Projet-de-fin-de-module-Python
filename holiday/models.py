from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date_start = models.DateField()
    date_end = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name