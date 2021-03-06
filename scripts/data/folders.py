#!/usr/bin/env python

import os
import sys

import django

sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'repositext.settings'
django.setup()

from django.contrib.auth.models import User  # noqa E402
from apps.repo.models import Folder  # noqa E402

ADD_TEST_FOLDERS = True

admin_user = User.objects.get(username='admin')

init_folders = [
    {
        'name': '-ROOT-',
        'description': 'System root folder.',
        'owner': admin_user,
    }
]


class FolderLoader:

    def _get_root_folder(self):
        return Folder.objects.get(name='-ROOT-')

    def add_init_folders(self):
        for each in init_folders:
            folder = Folder()
            for k, v in each.items():
                setattr(folder, k, v)
            folder.save()

    def add_test_folders(self, amount=3):
        for each in enumerate(range(amount), 1):
            folder = Folder()
            folder.name = f'TestFolder-{each[0]}'
            folder.description = f'Test Folder #{each[0]}'
            folder.owner = admin_user
            folder.parent = self._get_root_folder()
            folder.save()

    def run(self):
        self.add_init_folders()
        if ADD_TEST_FOLDERS:
            self.add_test_folders()


if __name__ == '__main__':
    folder_loader = FolderLoader()
    folder_loader.run()
