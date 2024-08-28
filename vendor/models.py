from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Vendor(models.Model):
  
    vendor_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    activeFlag = models.BooleanField(default=False)
    lastChangedUser = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'vendor'
        
class VendorParts(models.Model):
    id = models.AutoField(primary_key=True)
    activeFlag = models.BooleanField(default=False)
    lastcost = models.DecimalField(max_digits=28, decimal_places=9, null=True, blank=True)
    lastDate = models.DateTimeField(null=True, blank=True)
    leadTime = models.IntegerField(null=True, blank=True)
    part = models.ForeignKey('part.Parts', on_delete=models.CASCADE, null=True, blank=True)
    qtyMax = models.DecimalField(max_digits=28, decimal_places=9, null=True, blank=True)
    qtyMin = models.DecimalField(max_digits=28, decimal_places=9, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, default='Pending')
    uom = models.ForeignKey('uom.Uom', on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey('vendor.Vendor', on_delete=models.CASCADE, null=True, blank=True)
    vendorPartNumber = models.CharField(max_length=70, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'vendorparts'

    def __str__(self):
        return self.vendorPartNumber