from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, verbose_name='Student ID')
    student_name = models.CharField(max_length=150, verbose_name='Student Name')
    college = models.CharField(max_length=100, verbose_name='College Name')
    batch = models.PositiveIntegerField(verbose_name='Batch Year')
    semester = models.PositiveSmallIntegerField(verbose_name='Semester')
    student_photo = models.ImageField(upload_to='student_photos/', verbose_name='Student Photo', null=True, blank=True)

    def __str__(self):
        return f"{self.student_name} ({self.student_id})"
