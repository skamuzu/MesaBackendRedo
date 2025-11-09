from django.db import models

# Create your models here.
class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"   
        STUDENT = "STUDENT", "Student"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"
    
    clerkID = models.CharField(max_length=255, unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    role =models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
