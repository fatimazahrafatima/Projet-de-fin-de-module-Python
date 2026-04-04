from django.db import models
from home_auth.models import CustomUser
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    joining_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"    