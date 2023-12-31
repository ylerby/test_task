# Generated by Django 4.2.5 on 2023-09-24 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_task_app', '0006_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('col_id', models.IntegerField()),
                ('raw_id', models.IntegerField()),
                ('data', models.CharField()),
                ('file_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_task_app.csvfiles')),
            ],
        ),
        migrations.DeleteModel(
            name='CSVData',
        ),
    ]
