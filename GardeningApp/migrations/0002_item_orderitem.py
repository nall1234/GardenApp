# Generated by Django 2.2 on 2021-04-27 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GardeningApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_title', models.CharField(max_length=20)),
                ('item_description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('item_photo', models.ImageField(blank=True, default='items/blank.jpg', null=True, upload_to='items/')),
                ('item_quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_owned', to='GardeningApp.User')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_in_cart', to='GardeningApp.Item')),
                ('users_that_added', models.ManyToManyField(related_name='item_user_added', to='GardeningApp.User')),
            ],
        ),
    ]
