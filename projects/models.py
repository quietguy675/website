from django.db import models

# Create your models here.
class Project(models.Model):
    project_title = models.CharField(max_length=200)
    project_description = models.CharField(max_length=10000)
    pub_date = models.DateTimeField('date published')    


    def __str__(self):
        return self.project_title

class Choice(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    commenter_name = models.CharField(max_length=20)
    commenter_description = models.CharField(max_length=200)

