#!/usr/bin/env python

import os
import sys
from pathlib import Path
import subprocess

import django

# Deletes
# - django_home/*/migrations/*.py
# - django_home/GuidePlatform_Databases/*.sqlite3

estim_proj_home = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)
database_folder = os.path.join(estim_proj_home, "UCSD_IAB_DB")
# print(estim_proj_home, str(estim_proj_home))

for dir2nd_b in os.listdir(estim_proj_home):
    dir2nd = os.path.join(estim_proj_home, dir2nd_b)
    if os.path.isdir(dir2nd) and not dir2nd_b.startswith("."):
        # dir2nd may be a file.
        migration_dir = os.path.join(dir2nd, "migrations")
        # print("Check", migration_dir)
        if os.path.isdir(migration_dir):
            for cdir, fdirs_b, ffiles_b in os.walk(migration_dir):
                for ifile_b in ffiles_b:
                    filpath = os.path.join(cdir, ifile_b)
                    if (os.path.isfile(filpath) and
                            ifile_b.lower().endswith(".py") and
                            ifile_b.lower() != "__init__.py"):
                        os.remove(filpath)
                        print("Deleted migration-related file:", filpath)

os.makedirs(database_folder, exist_ok = True)
for file3rd_b in os.listdir(database_folder):
    filpath = os.path.join(database_folder, file3rd_b)
    if (os.path.isfile(filpath) and
            file3rd_b.lower().endswith("sqlite3")):
        os.remove(filpath)
        print("Deleted sqlite file:", filpath)

if estim_proj_home not in sys.path:
    sys.path.insert(0, estim_proj_home)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UCSD_IAB_Hermit1.settings')
django.setup()

os.chdir(estim_proj_home)
# print(os.getcwd())
coms = (
    [ "python", "./manage.py", "makemigrations" ],
    [ "python", "./manage.py", "makemigrations", "AccAuth_TZ"],
    [ "python", "./manage.py", "makemigrations", "appNichoAnu" ],
    [ "python", "./manage.py", "migrate" ],
    [ "python", "./manage.py", "migrate", "--database=nichoanu" ],
)

for icom in coms:
    print("--- Invoking :", " ".join(icom))
    subprocess.run(icom) # shell = True?

from django.contrib.auth.models import User
User.objects.all().delete()
User.objects.create_superuser('rsaito',
                              'golgo8128@yahoo.co.jp',
                              'aaaaaa')

# User.objects.create_user(username = "...",
#                          email    = "...",
#                          password = '...')