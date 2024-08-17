from django.db import models

# contact model
class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    sub = models.CharField(max_length=100,null=True,blank=True)
    text = models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return self.name
