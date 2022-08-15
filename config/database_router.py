from django.conf import settings

DJANGO_SCHEMA_NAME = settings.DJANGO_SCHEMA_NAME
RCCE_PRODUCTION_SCHEMA_NAME = settings.RCCE_PRODUCTION_SCHEMA_NAME
RCCE_VISUALIZATION_SCHEMA_NAME = settings.RCCE_VISUALIZATION_SCHEMA_NAME


class DjangoRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'auth', 'contenttypes', 'admin', 'sessions', 'migrate_csv'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return DJANGO_SCHEMA_NAME
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return DJANGO_SCHEMA_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        django database.
        """
        if app_label in self.route_app_labels:
            return db == DJANGO_SCHEMA_NAME
        return None


class RcceVisualizationRouter:
    """
    A router to control all database operations on models in the visualization application.
    """
    route_app_labels = {'visualization', }

    def db_for_read(self, model, **hints):
        """
        Attempts to read visualization models go to rcce visualization.
        """
        if model._meta.app_label in self.route_app_labels:
            return RCCE_VISUALIZATION_SCHEMA_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the visualization
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None


class RcceProductionRouter:
    """
    A router to control all database operations on models rcce production
    we have read write access on few tables only, we don't create/update any
    tables definitions on production database.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read rcce production.
        """
        if model._meta.app_label in self.route_app_labels:
            return RCCE_PRODUCTION_SCHEMA_NAME
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write production database
        """
        if model._meta.app_label in self.route_app_labels:
            return RCCE_PRODUCTION_SCHEMA_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the production database.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None
