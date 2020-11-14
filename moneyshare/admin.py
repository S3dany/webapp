from django.contrib import admin
from .models import Person, Group, Bill, FriendRequest, Item, Share

admin.site.register(Person)

admin.site.register(Group)

admin.site.register(FriendRequest)

admin.site.register(Share)

admin.site.register(Item)

admin.site.register(Bill)

# Register your models here.
