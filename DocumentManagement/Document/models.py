from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import magic
from django.utils import timezone

ext_validator = FileExtensionValidator(['png', 'jpg', 'pdf', 'docx'])


def validate_file_mimetype(file):
    limit = 2 * 1024 * 1024
    accept = ['image/png', 'image/jpg', 'image/jpeg', 'application/pdf', 'application/docx']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in accept:
        raise ValidationError("Unsupported file type")
    elif file.size > limit:
        raise ValidationError("File too large. Size should not exceed 2MB.")


class FileUpload(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='fileupload/', validators=[ext_validator, validate_file_mimetype])
    description = models.CharField(max_length=500)
    file_formate = models.CharField(max_length=30, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(default=timezone.now)

    def delete(self):
        self.file.delete()
        super().delete()


class FileShare(models.Model):
    file = models.ForeignKey('FileUpload', on_delete=models.CASCADE)
    share_with = models.ForeignKey(User, on_delete=models.CASCADE)