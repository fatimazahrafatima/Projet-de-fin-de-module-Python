from django.db import models

class Department(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    department_image = models.ImageField(upload_to='photos/',blank=True)

    def __str__(self):
        return self.name