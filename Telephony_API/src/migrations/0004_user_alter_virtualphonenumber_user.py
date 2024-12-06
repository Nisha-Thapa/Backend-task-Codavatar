# Generated by Django 5.1.4 on 2024-12-06 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0003_alter_virtualphonenumber_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='virtualphonenumber',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_numbers', to='src.user'),
        ),
    ]