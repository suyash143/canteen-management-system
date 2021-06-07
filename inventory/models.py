from django.db import models
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver


class Supplies(models.Model):
    name=models.CharField(max_length=500,null=True,blank=True)
    stock=models.FloatField(null=True,blank=True)
    minimum=models.FloatField(null=True,blank=True)
    created = models.DateTimeField(null=True)


class Order(models.Model):
    amount=models.IntegerField(null=True,blank=True)
    ordered_by=models.ForeignKey(User,on_delete=models.SET_NULL, null=True,related_name='order_by',blank=True)
    items=models.IntegerField(null=True,blank=True)
    created=models.DateTimeField(null=True,blank=True)
    taken_by=models.ForeignKey(User,on_delete=models.SET_NULL, null=True,related_name='taken_by',blank=True)
    transaction_id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    transaction_mode=models.CharField(max_length=500,null=True,blank=True)



class Info(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile=models.IntegerField(null=True,blank=True)
    address=models.CharField(max_length=500,blank=True,null=True)
    credit=models.IntegerField(null=True,blank=True,default=0)
    birthdate=models.DateField(null=True, blank=True)
    profile=models.CharField(max_length=400,null=True,blank=True)
    otp = models.CharField(max_length=500, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Info.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.info.save()
