# Generated by Django 5.2.1 on 2025-05-22 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboardmanager', '0013_alter_testimonial_options_testimonial_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='order',
            field=models.PositiveIntegerField(blank=True, help_text='Display order (lower numbers appear first). Leave blank to add to the end.', null=True),
        ),
    ]
