# Generated by Django 5.1.6 on 2025-04-08 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0004_alter_cafe_image_alter_cafe_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='address',
            field=models.TextField(blank=True, default='No address provided', null=True),
        ),
    ]
