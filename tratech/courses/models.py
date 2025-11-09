from django.db import models
from users.models import User


# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.URLField(blank=True, null=True)
    course_number = models.IntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.course_number:
            last = Course.objects.all().order_by("-course_number").first()
            self.course_number = (last.course_number if last else 0) + 1
        super().save(*args, **kwargs)


class CourseInstructor(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="instructors"
    )
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "course_instructors"
        unique_together = (
            "course",
            "instructor",
        )  # optional if you want to prevent duplicates

    def __str__(self):
        return f"{self.instructor.username} → {self.course.title}"
