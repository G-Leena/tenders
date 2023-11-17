from django.db import models

class Payment(models.Model):
    txnid=models.AutoField(primary_key=True)
    uid=models.CharField(max_length=50)
    amt=models.CharField(max_length=50)
    info=models.CharField(max_length=50)