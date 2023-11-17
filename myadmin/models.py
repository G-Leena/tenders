from django.db import models

class Category(models.Model):
    catid=models.AutoField(primary_key=True)
    catname=models.CharField(max_length=50,unique=True)
    caticonname=models.CharField(max_length=100)

class SubCategory(models.Model):
    subcatid=models.AutoField(primary_key=True)
    catname=models.CharField(max_length=50)
    subcatname=models.CharField(max_length=50,unique=True)
    subcaticonname=models.CharField(max_length=100)

class Tenders(models.Model):
    tenderid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50)
    subcatname=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    ldate=models.CharField(max_length=10)
    edate=models.CharField(max_length=10)
    info=models.CharField(max_length=50)