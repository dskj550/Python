from django.db import models

# Create your models here.

class User(models.Model):
    class Meta:
        db_table = 'user'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=48,null=False)
    email = models.CharField(max_length=48,null=False,unique=True)
    password = models.CharField(max_length=128,null=False)

    def __repr__(self):
        return "<User {} {}>".format(self.id,self.name)




