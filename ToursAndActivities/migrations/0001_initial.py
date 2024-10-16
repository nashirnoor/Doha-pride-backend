# Generated by Django 4.2 on 2024-10-16 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TopActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=800)),
                ('image', models.ImageField(upload_to='top_activities/')),
            ],
        ),
        migrations.CreateModel(
            name='TourImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tours/')),
                ('alt_text', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ToursAndActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=3000)),
                ('min_age', models.PositiveIntegerField(default=0)),
                ('max_age', models.PositiveIntegerField(default=100)),
                ('passengers_count', models.PositiveIntegerField(default=1)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True)),
                ('price', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('media_gallery', models.ManyToManyField(blank=True, related_name='tours', to='ToursAndActivities.tourimage')),
            ],
        ),
    ]
