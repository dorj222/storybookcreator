# Generated by Django 4.2.7 on 2023-12-08 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storybook', '0006_alter_image_id_alter_storybook_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
