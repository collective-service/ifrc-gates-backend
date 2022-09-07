from django.conf import settings


class CustomDBRouter:
    route_app_labels = {
        app_label: database
        for database, app_labels in [
            (settings.RCCE_PRODUCTION_DB, ('data',)),
            (settings.RCCE_VISUALIZATION_DB, ('visualization',)),
            (settings.DJANGO_DB, ('auth', 'contenttypes', 'admin', 'sessions', 'migrate_csv',)),
        ]
        for app_label in app_labels
    }

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        return self.route_app_labels.get(model._meta.app_label)

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        return self.route_app_labels.get(model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        return (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        )

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        django database.
        NOTE: Migrate operation are skipped silently but will be tracked (fake) in django_migrations table.
        """
        return self.route_app_labels.get(app_label) == settings.DJANGO_DB
