# Generated by Django 2.2.5 on 2024-06-14 04:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_delete_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='overview',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='概要'),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
