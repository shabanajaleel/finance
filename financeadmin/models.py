from django.db import models

# Create your models here.
class project(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name

class partner(models.Model):
    partner_name=models.CharField(max_length=30)
    

    def __str__(self):
        return self.partner_name

class partnership(models.Model):
    project=models.ForeignKey(project,on_delete=models.CASCADE)
    partner=models.ForeignKey(partner,on_delete=models.CASCADE,null=True)
    partnership=models.IntegerField()

    def __str__(self):
        return str(self.partner)

class profit(models.Model):
    created_date=models.DateField()
    project=models.ForeignKey(project,on_delete=models.CASCADE)
    amount=models.BigIntegerField()

    def __str__(self):
        return str(self.project)
