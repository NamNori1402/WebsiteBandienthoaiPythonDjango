# Generated by Django 5.1.1 on 2024-09-17 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
    ]
