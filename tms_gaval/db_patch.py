# tms_gaval/db_patch.py
import warnings
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.postgresql.base import DatabaseWrapper as PostgreSQLDatabaseWrapper

# Define la función set_schema si no existe en BaseDatabaseWrapper
# Esta es una función genérica que django-tenants espera
if not hasattr(BaseDatabaseWrapper, 'set_schema'):
    def set_schema(self, schema_name):
        if schema_name is None:
            schema_name = 'public'
        cursor = self.cursor()
        cursor.execute(f"SET search_path to {schema_name}")

    BaseDatabaseWrapper.set_schema = set_schema
    warnings.warn(
        "Monkey-patched BaseDatabaseWrapper.set_schema. "
        "This is a workaround for django-tenants compatibility issues "
        "with certain database drivers or Python versions. "
        "Consider upgrading django-tenants or your DB driver if possible.",
        RuntimeWarning
    )

# Define la función set_tenant si no existe en PostgreSQLDatabaseWrapper
# Esta es una función específica para PostgreSQL que django-tenants espera
if not hasattr(PostgreSQLDatabaseWrapper, 'set_tenant'):
    def set_tenant(self, tenant):
        self.set_schema(tenant.schema_name)
    PostgreSQLDatabaseWrapper.set_tenant = set_tenant
    warnings.warn(
        "Monkey-patched PostgreSQLDatabaseWrapper.set_tenant. "
        "This is a workaround for django-tenants compatibility issues "
        "with certain database drivers or Python versions. "
        "Consider upgrading django-tenants or your DB driver if possible.",
        RuntimeWarning
    )