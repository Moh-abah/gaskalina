# Generated by Django 5.1.3 on 2025-07-08 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_driver_identitynumber_user_fullname_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('notes', models.TextField(blank=True, null=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='users.driver')),
            ],
        ),
    ]
