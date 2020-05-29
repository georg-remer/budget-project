# Generated by Django 2.2.6 on 2019-11-05 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_budget', '0003_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('sum', models.DecimalField(decimal_places=2, max_digits=9)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=9)),
                ('income', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='income', to='monthly_budget.Category')),
                ('outcome', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='outcome', to='monthly_budget.Category')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='monthly_budget.Period')),
            ],
        ),
    ]