# Generated by Django 2.1.7 on 2019-05-28 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_auto_20190526_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='サムネイル（空欄可）'),
        ),
    ]
