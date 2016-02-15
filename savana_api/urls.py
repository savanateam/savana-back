# Copyright (C) 2015-2016 Dario marinoni <marinoni.dario@gmail.com>
# Copyright (C) 2015-2016 Luca Sturaro <hcsturix74@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from .routers import router
from taiga.contrib_routers import router as contrib_router


from productships.api import ProductIncrementViewSet, ProductIncrementVotersViewSet,\
    ProductIncrementWatchersViewSet, ProductIncrementAttachmentViewSet

admin.site.site_header = "Savana"

router.register(r"increments", ProductIncrementViewSet, base_name="increments")
router.register(r"increments/(?P<resource_id>\d+)/watchers", ProductIncrementWatchersViewSet, base_name="increments-watchers")
router.register(r"increments/(?P<resource_id>\d+)/voters", ProductIncrementVotersViewSet, base_name="increments-voters")

router.register(r"productincrements/attachments", ProductIncrementAttachmentViewSet, base_name="productincrement-attachments")


##############################################
# Default
##############################################

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(contrib_router.urls)),
    url(r'^api/v1/api-auth/', include('taiga.base.api.urls', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
]

handler500 = "taiga.base.api.views.api_server_error"


##############################################
# Front sitemap
##############################################

if settings.FRONT_SITEMAP_ENABLED:
    from django.contrib.sitemaps.views import index
    from django.contrib.sitemaps.views import sitemap
    from django.views.decorators.cache import cache_page

    from taiga.front.sitemaps import sitemaps

    urlpatterns += [
        url(r"^front/sitemap\.xml$",
            cache_page(settings.FRONT_SITEMAP_CACHE_TIMEOUT)(index),
            {"sitemaps": sitemaps, 'sitemap_url_name': 'front-sitemap'},
            name="front-sitemap-index"),
        url(r"^front/sitemap-(?P<section>.+)\.xml$",
            cache_page(settings.FRONT_SITEMAP_CACHE_TIMEOUT)(sitemap),
            {"sitemaps": sitemaps},
            name="front-sitemap")
    ]


##############################################
# Static and media files in debug mode
##############################################

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    def mediafiles_urlpatterns(prefix):
        """
        Method for serve media files with runserver.
        """
        import re
        from django.views.static import serve

        return [
            url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve,
                {'document_root': settings.MEDIA_ROOT})
        ]

    # Hardcoded only for development server
    urlpatterns += staticfiles_urlpatterns(prefix="/static/")
    urlpatterns += mediafiles_urlpatterns(prefix="/media/")
