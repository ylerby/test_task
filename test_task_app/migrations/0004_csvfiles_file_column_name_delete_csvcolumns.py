# Generated by Django 4.2.5 on 2023-09-12 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_task_app', '0003_csvfiles_file_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvfiles',
            name='file_column_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CSVColumns',
        ),
    ]