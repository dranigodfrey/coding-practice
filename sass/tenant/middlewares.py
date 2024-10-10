from django.db import connection
from client.models import Client
from django_tenants.middleware import TenantMainMiddleware


class RequestIDTenantMiddleware(TenantMainMiddleware):
    def process_request(self, request):
        connection.set_schema_to_public()
        hostname = self.hostname_from_request(request)

        x_request_id = request.META.get('HTTP_X_REQUEST_ID')
        try:
            tenant_model = Client.objects.get(uuid=x_request_id)
        except Client.DoesNotExist:
            return
        request.tenant = tenant_model
        connection.set_tenant(request.tenant)