import uuid

from django.contrib.auth.models import User
from django.db import models


class UuidPrimaryKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Timestamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Folder(UuidPrimaryKey, Timestamped):
    name = models.CharField('Name', max_length=255)
    parent = models.ForeignKey(
        'Folder', on_delete=models.CASCADE,
        null=True, blank=True
    )
    description = models.TextField('Description', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DocumentVersion(UuidPrimaryKey, Timestamped):
    version = models.CharField('Version', max_length=11)
    content_file = models.FileField(
        'Content File', upload_to='content/%Y/%m/%d/'
    )
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'Document', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.parent.name}:{self.version}'


class Document(UuidPrimaryKey, Timestamped):
    name = models.CharField('Name', max_length=255)
    parent = models.ForeignKey(
        'Folder', on_delete=models.CASCADE
    )
    description = models.TextField('Description', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    versions = models.ManyToManyField(
        DocumentVersion, blank=True
    )

    def __str__(self):
        return self.name
