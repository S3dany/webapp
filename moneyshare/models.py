import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.shortcuts import redirect


class FriendRequest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default="0")
    timestamp = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=250, unique=True, default='Group')
    Creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Bill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    bill_name = models.CharField(max_length=250, default='Bill')
    bill_maker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bill_maker', on_delete=models.CASCADE)
    bill_group = models.ForeignKey(Group, blank=True, related_name='group_bills')
    no_items = models.IntegerField(default='1')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bill_name


class Person(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2, default="0")
    friends = models.ManyToManyField("self", blank=True, related_name='userfriends')
    myGroups: Group = models.ManyToManyField(Group, related_name='myGroups')
    friendRequests = models.ManyToManyField(FriendRequest, blank=True, related_name='userfriendrequests')
    transactions = models.ManyToManyField(Transaction, blank=True, related_name='userTransections')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_person(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_person(sender, instance, **kwargs):
    instance.person.save()


class Item(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    item_bill = models.ForeignKey(Bill, blank=True, related_name='billitems')
    item_name = models.CharField(max_length=250, default='Item')
    price = models.DecimalField(max_digits=9, decimal_places=2, default="0")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name


