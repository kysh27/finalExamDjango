from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)

    # Override the __unicode__() method
    def __unicode__(self):
        return self.user.username
    
    def __str__(self):
        return self.user.username


class AddressBook(models.Model):
    useridfk = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fName = models.CharField(max_length = 50)
    lName = models.CharField(max_length = 50)
    contactNum = models.CharField(max_length = 20)
    address = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.fName


### block for CSV
