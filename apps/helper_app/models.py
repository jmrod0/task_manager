from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
 
class Job(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    location = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    creator = models.ForeignKey(User, related_name = 'created_jobs', on_delete = models.CASCADE)
    workers = models.ManyToManyField(User, related_name ='jobs')
