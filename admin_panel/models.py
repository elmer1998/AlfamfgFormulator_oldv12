from django.db import models
from django.contrib.auth.models import User
from admin_helpers.models import Staging
from part.models import Parts
from utilities.models import Category, ProductFormat, ProductQualities, ProductType, SubCategory

# Create your models here.

class FolderFormula(models.Model):
  
    folder_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'folder_formula'
        
class Formula(models.Model):

    formula_name = models.CharField(max_length=255, null=True, blank=True)
    brand_name = models.CharField(max_length=255, null=True, blank=True)
    formula_num = models.CharField(max_length=255, null=True, blank=True)
    upc = models.CharField(max_length=255, null=True, blank=True)
    assigned_folder = models.ForeignKey(FolderFormula, on_delete=models.CASCADE, null=True, blank=True, related_name='formulas')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True, blank=True)
    product_format = models.ForeignKey(ProductFormat, on_delete=models.CASCADE, null=True, blank=True)
    formula_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_quality = models.ManyToManyField(ProductQualities, blank=True)  
    
    parts = models.ManyToManyField(Parts, blank=True)
    sortOrder = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'formula'
        
class Formula_Ingredients(models.Model):

    ingredient_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    formula = models.ForeignKey(Formula, on_delete=models.CASCADE, null=True, blank=True)
    sortOrder = models.IntegerField(blank=True, null=True)
    staging = models.ForeignKey(Staging, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'formula_ingredients'
