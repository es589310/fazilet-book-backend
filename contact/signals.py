from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
# SiteSettings artıq contact app-də yoxdur, settings app-ə köçürüldü
import logging

logger = logging.getLogger(__name__)

# Logo-lar artıq settings app-də idarə olunur 