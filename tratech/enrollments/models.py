from django.db import models


# Create your models here.
class Enrollment(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Courses", on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} enrolled in {self.course.course_name}"

    class Meta:
        db_table = "enrollments"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"], name="unique_user_course_enrollment"
            )
        ]
