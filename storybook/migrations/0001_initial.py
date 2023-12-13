# Generated by Django 4.2.7 on 2023-12-10 15:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Storybook',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('createdAt', models.DateTimeField()),
                ('duration', models.FloatField()),
                ('iterations', models.IntegerField()),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='storybook_images/')),
                ('storybook_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='storybook.storybook')),
            ],
        ),
    ]
