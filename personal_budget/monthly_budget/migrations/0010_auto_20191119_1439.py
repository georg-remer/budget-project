# Generated by Django 2.2.6 on 2019-11-19 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_budget', '0009_auto_20191119_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='default_planned_sum',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
    ]