# Generated by Django 2.2.6 on 2019-11-04 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginning', models.DateField()),
                ('ending', models.DateField()),
            ],
        ),
    ]
