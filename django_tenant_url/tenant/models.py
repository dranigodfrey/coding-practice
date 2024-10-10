from django_tenants_url.models import TenantMixin, DomainMixin, TenantUserMixin


class Client(TenantMixin):
    pass


class Domain(DomainMixin):
    pass


class TenantUser(TenantUserMixin):
    pass
