from django.db import models
from department.models import Department

class Teacher(models.Model):
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    teacher_id    = models.CharField(max_length=20)
    gender        = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15)
    email         = models.EmailField(max_length=100, blank=True)
    address       = models.TextField(blank=True)
    subject       = models.CharField(max_length=100)
    joining_date  = models.DateField(null=True, blank=True)
    teacher_image = models.ImageField(upload_to='teachers/', blank=True)
    department    = models.ForeignKey(
                      Department,
                      on_delete=models.SET_NULL,
                      null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"