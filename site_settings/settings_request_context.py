
from django.template import RequestContext

from site_settings.models import SiteSettings


def global_settings(request):
    site_settings = SiteSettings.objects.all()[:1]
    return {"site_settings": site_settings}
