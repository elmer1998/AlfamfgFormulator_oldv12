
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Parts(models.Model):

    part_num = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    trade_name = models.CharField(max_length=255, null=True, blank=True)
    manufacturer_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    inventory_category = models.CharField(max_length=255, null=True, blank=True)
    packaging_type = models.CharField(max_length=255, null=True, blank=True)
    chemical_type = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    activeFlag = models.BooleanField(default=False)
    lastChangedUser = models.CharField(max_length=255, null=True, blank=True)

    std_cost = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'part'
        
class PartDocument(models.Model):
    file = models.FileField(upload_to='')
    type = models.CharField(max_length=255, null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    vendorparts = models.ForeignKey('vendor.VendorParts', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=255, default='In Progress')
    notes = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'part_document'
        
class PartCost(models.Model):
    avg_cost = models.DecimalField(max_digits=28, decimal_places=9)
    part = models.OneToOneField('part.Parts', on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=28, decimal_places=9)
    total_cost = models.DecimalField(max_digits=28, decimal_places=9)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'part_cost'
        
    def __str__(self):
        return f'PartCost(id={self.id}, part_id={self.part_id})'
