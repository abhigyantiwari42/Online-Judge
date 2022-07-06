from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    Firstname=models.CharField(max_length=20)
    Lastname=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=30)

    def __str__(self):
        return self.Firstname


class Problem(models.Model):
   problemid=models.CharField(("ID"), max_length=50)
   problemname=models.CharField(("name"), max_length=50)
   description=models.CharField(max_length=300)
   score=models.IntegerField(default=0)

   def __str__(self):
       return str(self.problemid) + " " +self.problemname

class Submission(models.Model):
    problemid=models.ForeignKey(Problem, on_delete=models.CASCADE)
    answercode=models.CharField(max_length=300)
    submissiontime=models.TimeField(default=timezone.now)
    verdict=models.CharField(max_length=20)
  
    def __str__(self):
       return str(self.problemid) + str(self.submissiontime)

class Testcase(models.Model):
    problemid=models.ForeignKey(Problem,on_delete=models.CASCADE)
    inputdoc=models.CharField(max_length=500)
    outputdoc=models.CharField(max_length=500)

    def __str__(self):
       return str(self.problemid)


