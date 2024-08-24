from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class UOM(models.Model):
    active_flag = models.BooleanField()  # maps to `activeFlag`
    code = models.CharField(max_length=10, unique=True)
    default_record = models.BooleanField()  # maps to `defaultRecord`
    description = models.CharField(max_length=256)
    integral = models.BooleanField()
    name = models.CharField(max_length=30, unique=True)
    read_only = models.BooleanField()  # maps to `readOnly`
    uom_type = models.ForeignKey('UOMType', on_delete=models.CASCADE)  # maps to `uomType`

    class Meta:
        db_table = 'uom'
        
from django.db import models

class UOMConversion(models.Model):
    description = models.CharField(max_length=256)
    factor = models.FloatField(null=True, blank=True)  # maps to `double DEFAULT NULL`
    from_uom = models.ForeignKey('UOM', related_name='from_uom_conversions', on_delete=models.CASCADE)  # maps to `fromUomId`
    multiply = models.FloatField(null=True, blank=True)  # maps to `double DEFAULT NULL`
    to_uom = models.ForeignKey('UOM', related_name='to_uom_conversions', on_delete=models.CASCADE)  # maps to `toUomId`

    class Meta:
        db_table = 'uomconversion'

    def __str__(self):
        return self.description

from django.db import models

class UOMType(models.Model):
    name = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'uomtype'

    def __str__(self):
        return self.name
