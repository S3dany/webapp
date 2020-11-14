# Generated by Django 2.2.7 on 2020-02-05 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('item_name', models.CharField(default='Item', max_length=250)),
                ('price', models.DecimalField(decimal_places=2, default='0', max_digits=9)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=250, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default='0', max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.DecimalField(decimal_places=2, default='0', max_digits=9)),
                ('friends', models.ManyToManyField(blank=True, related_name='userfriends', to=settings.AUTH_USER_MODEL)),
                ('shares', models.ManyToManyField(blank=True, related_name='shares', to='moneyshare.Share')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Group', max_length=250, unique=True)),
                ('current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='moneyshare.Person')),
                ('myGroup', models.ManyToManyField(related_name='myGroup', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('bill_name', models.CharField(default='Bill', max_length=250)),
                ('group', models.CharField(default='', max_length=250)),
                ('no_items', models.IntegerField(default='1')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bill_maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_maker', to=settings.AUTH_USER_MODEL)),
                ('items', models.ManyToManyField(blank=True, related_name='billitems', to='moneyshare.Item')),
                ('people_to_share', models.ManyToManyField(blank=True, related_name='people_to_share', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
