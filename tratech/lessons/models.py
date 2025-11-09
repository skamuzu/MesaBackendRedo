from django.db import models


# Create your models here.
class Lessons(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey("courses.Courses", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    lesson_number = models.IntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.lesson_number:
            last = Lessons.objects.all().order_by('-lesson_number').first()
            self.lesson_number = (last.lesson_number if last else 0) + 1
        super().save(*args, **kwargs)