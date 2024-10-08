# Generated by Django 5.1 on 2024-09-04 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_dog_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='neutered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dog',
            name='status',
            field=models.CharField(choices=[('N', 'Not Adopted'), ('A', 'Adopted'), ('I', 'Interest')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='vacination',
            name='vacinations',
            field=models.CharField(max_length=100),
        ),
    ]
