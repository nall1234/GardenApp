# Generated by Django 2.2 on 2021-04-28 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GardeningApp', '0004_remove_orderitem_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='users_that_added',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='users_that_added',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='item_user_added', to='GardeningApp.User'),
            preserve_default=False,
        ),
    ]
