# Generated by Django 2.1.7 on 2019-03-24 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blog_img'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-created_time']},
        ),
        migrations.AlterField(
            model_name='blog',
            name='img',
            field=models.ImageField(upload_to='img'),
        ),
    ]
