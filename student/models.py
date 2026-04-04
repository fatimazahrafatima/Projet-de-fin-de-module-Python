from django.db import models
from subject.models import Subject
from home_auth.models import CustomUser
class ExamResult(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]

    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='exam_results'
    )

    exam = models.ForeignKey(
        'Exam',
        on_delete=models.CASCADE,
        related_name='results'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    grade = models.FloatField(
        null=True,
        blank=True,
        help_text="Grade in percentage or marks"
    )

    class Meta:
        unique_together = ['student', 'exam']  # Prevent duplicate result for same student & exam

    def __str__(self):
        return f"{self.student} - {self.exam} : {self.status}"
class Exam(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE)

    title = models.CharField(max_length=100 )
    exam_type = models.CharField(max_length=10,choices=[('Midterm', 'Midterm'), ('Final', 'Final'),('quiz', 'quiz')],
        default='quiz')
    
    exam_date = models.DateTimeField()

    duration = models.DurationField(help_text="exam duration")

    total_marks = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.title} - {self.subject.name}"

class Parent(models.Model):
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_mobile = models.CharField(max_length=15)
    father_email = models.EmailField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_mobile = models.CharField(max_length=15)
    mother_email = models.EmailField(max_length=100)
    present_address = models.TextField()
    permanent_address = models.TextField()

    def __str__(self):
        return f"{self.father_name} & {self.mother_name}"


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    gender = models.CharField(max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField()
    student_class = models.ManyToManyField(Subject)
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    admission_number = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    parent = models.OneToOneField(Parent, on_delete=models.CASCADE)
    student_image = models.ImageField(upload_to='photos/',blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
