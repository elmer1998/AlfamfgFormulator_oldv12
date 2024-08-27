import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Generated_Reports

@receiver(post_delete, sender=Generated_Reports)
def delete_report_file(sender, instance, **kwargs):
    file_path = instance.get_file_path()
    if os.path.exists(file_path):
        os.remove(file_path)
