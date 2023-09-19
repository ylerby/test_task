from django.db import models


class CSVFiles(models.Model):
    file_name = models.CharField(max_length=255)
    file_url = models.URLField(max_length=255)
    file_column_name = models.CharField(max_length=255)


class CSVData(models.Model):
    column_id = models.ForeignKey(CSVFiles, on_delete=models.CASCADE)
    column_data = models.CharField(max_length=255)


'''class CSVFileInfo(models.Model):
    column_id = models.IntegerField()
'''

'''class CSVColumns(models.Model):
    file = models.ForeignKey(CSVFiles, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=255)'''
