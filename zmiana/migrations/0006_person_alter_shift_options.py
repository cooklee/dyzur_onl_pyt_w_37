# Generated by Django 5.1.3 on 2024-11-24 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zmiana', '0005_shift_unique_shift_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='shift',
            options={'ordering': ['date']},
        ),
    ]