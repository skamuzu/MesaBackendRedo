from django.db import models

# Create your models here.
class Modules(models.Model):
    module_name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey("courses.Courses", on_delete=models.CASCADE)
    module_number = models.IntegerField(unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.module_name
    
    def save(self, *args, **kwargs):
        if not self.module_number:
            last = Modules.objects.all().order_by('-module_number').first()
            self.module_number = (last.module_number if last else 0) + 1
        super().save(*args, **kwargs)