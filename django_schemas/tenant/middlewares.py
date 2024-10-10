import logging
from django_tenants.utils import get_tenant_model, get_public_schema_name
from django.db import connection
from django.http import Http404

logger = logging.getLogger(__name__)

class SubdirectoryTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get tenant slug from URL
        path = request.path.split('/')
        tenant_slug = path[1] if len(path) > 1 else None
        
        logger.info(f"Extracted tenant slug: {tenant_slug}")

        TenantModel = get_tenant_model()

        if not tenant_slug or tenant_slug == get_public_schema_name():
            # Use public schema if no tenant
            connection.set_schema_to_public()
        else:
            try:
                # Try to find tenant by slug
                tenant = TenantModel.objects.get(schema_name=tenant_slug)
                connection.set_tenant(tenant)
            except TenantModel.DoesNotExist:
                logger.error(f"Tenant '{tenant_slug}' does not exist")
                raise Http404(f"Tenant '{tenant_slug}' does not exist")

        response = self.get_response(request)
        return response
