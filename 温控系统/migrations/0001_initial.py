# Generated by Django 2.2.1 on 2019-06-08 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_num', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('user_type', models.CharField(choices=[('C', 'Customer'), ('F', 'Front'), ('A', 'AirCManager'), ('H', 'HotelManager')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='UseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user_name', models.CharField(max_length=30)),
                ('room_num', models.CharField(max_length=30)),
                ('temp', models.IntegerField()),
                ('wind', models.CharField(choices=[('L', 'Low'), ('M', 'Middle'), ('H', 'High')], max_length=5)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UserRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30)),
                ('room', models.CharField(max_length=30)),
                ('schedulingtimes', models.IntegerField(default=0)),
                ('reachtimes', models.IntegerField(default=0)),
            ],
        ),
    ]
