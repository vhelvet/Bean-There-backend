# Generated by Django 5.1.6 on 2025-04-23 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_id',
            field=models.CharField(default='temp', editable=False, max_length=12),
        ),
    ]
