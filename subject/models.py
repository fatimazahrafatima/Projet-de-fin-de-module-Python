from django.db import models
from department.models import Department
from teacher.models import Teacher

class Subject(models.Model):
    name        = models.CharField(max_length=100)
    code        = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    department  = models.ForeignKey(
                    Department, 
                    on_delete=models.CASCADE,
                    related_name='subjects')
    Teacher  = models.ForeignKey(
                    Teacher, 
                    on_delete=models.CASCADE,
                    related_name='subjects',
                    null=True
                    )
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"