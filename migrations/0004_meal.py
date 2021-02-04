# Generated by Django 2.2.9 on 2021-02-03 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kansas', '0003_auto_20210129_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('meal', models.CharField(choices=[('0', 'Breakfast'), ('1', 'Lunch'), ('2', 'Dinner')], default='2', max_length=9)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kansas.Recipe')),
            ],
            options={
                'unique_together': {('date', 'meal')},
            },
        ),
    ]
