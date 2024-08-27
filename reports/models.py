import os
from django.db import models

from alfamfg_formulator import settings

# Create your models here.

class Generated_Reports(models.Model):
    
    report_name = models.CharField(max_length=255, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'reports'
    
    def get_file_path(self):
        return os.path.join(settings.BASE_DIR, 'Generated Reports', self.report_name)

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        file_path = self.get_file_path()
        if os.path.exists(file_path):
            os.remove(file_path)
        super().delete(*args, **kwargs)