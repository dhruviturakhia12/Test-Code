# Generated by Django 4.0.3 on 2022-09-09 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='description',
            field=models.TextField(blank=True, max_length=250),
        ),
    ]
