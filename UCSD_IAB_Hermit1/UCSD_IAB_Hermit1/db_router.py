
# User accounts are stored in the default database.


class DB_Router:
    def db_for_read(self, model, **hints):

        if model._meta.app_label == "appNichoAnu":
            return "nichoanu"

    def db_for_write(self, model, **hints):

        if model._meta.app_label == "appNichoAnu":
            return "nichoanu"

    def allow_relation(self, obj1, obj2, **hints):

        if obj1._meta.app_label == 'appNichoAnu' or \
           obj2._meta.app_label == 'appNichoAnu':
           return True

    def allow_migrate(self, db, app_label, model=None, **hints):

        if app_label == "appNichoAnu":
            return db == "nichoanu"
