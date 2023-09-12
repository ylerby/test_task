from django.db import models


class User(models.Model):
    login = models.CharField()
    password = models.CharField()
    email = models.EmailField()


class CSVFiles(models.Model):
    file_name = models.CharField(max_length=255)
    file_url = models.URLField(max_length=255)
    file_column_name = models.CharField(max_length=255)

'''class CSVColumns(models.Model):
    file = models.ForeignKey(CSVFiles, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=255)'''
