# Generated by Django 2.1.3 on 2019-04-06 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0008_auto_20190406_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='meta_description',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
