# Generated by Django 5.2.1 on 2025-05-19 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboardmanager', '0011_rename_testimonial_image_testimonial_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='submitted_by',
        ),
    ]
