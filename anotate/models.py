from django.core.exceptions import MiddlewareNotUsed
from django.db import models

# Create your models here.

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=1000, null=True, blank=True)
    password = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user_name

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=1000, null=True, blank=True)
    project_user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name

class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to='static/uploads/images', null=True, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    image_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.image_id)