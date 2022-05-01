from django.db import models


class Position(models.Model):
    x = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    y = models.DecimalField(max_digits=12, decimal_places=2, null=False)


class Point(models.Model):
    id = models.IntegerField()
    description = models.CharField(max_length=512, blank=True, null=True)
    position = models.OneToOneField(Position, on_delete=models.CASCADE, primary_key=True)


class Data(models.Model):
    clusters = models.IntegerField()


