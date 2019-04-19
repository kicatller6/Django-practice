# Generated by Django 2.1.7 on 2019-04-09 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20190324_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Birthday'),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(help_text='Enter a natual language', max_length=20),
        ),
    ]