from django.db import models


class CSVFiles(models.Model):
    file_name = models.CharField(max_length=255)
    file_url = models.URLField(max_length=255)
    # file_column_name = models.CharField(max_length=255)


class ColumnData(models.Model):
    file_id = models.ForeignKey(CSVFiles, on_delete=models.CASCADE)
    col_id = models.IntegerField()
    raw_id = models.IntegerField()
    data = models.CharField()


'''class CSVFileInfo(models.Model):
    column_id = models.IntegerField()
'''

'''class CSVColumns(models.Model):
    file = models.ForeignKey(CSVFiles, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=255)'''
