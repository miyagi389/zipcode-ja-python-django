# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from rest_framework_swagger.views import get_swagger_view

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/docs/', permanent=True)),

    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),

    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browseable API.
    # url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # User App
    url(r'^api/v1/zipcode/jp/', include('zipcode_jp.urls.api')),

    # Swagger
    url(r'^docs/', get_swagger_view(title='API')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
