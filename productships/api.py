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

from django.apps import apps

from taiga.base import filters
from taiga.base import response
from taiga.base.decorators import detail_route
from taiga.base.api import ModelCrudViewSet, ModelListViewSet
from taiga.base.api.utils import get_object_or_404
from taiga.base.utils.db import get_object_or_none

from taiga.projects.notifications.mixins import WatchedResourceMixin, WatchersViewSetMixin
from taiga.projects.history.mixins import HistoryResourceMixin
from taiga.projects.attachments.api import BaseAttachmentViewSet

from . import serializers
from . import models
from . import permissions

import datetime


class ProductIncrementViewSet(
        HistoryResourceMixin,
        # WatchedResourceMixin,
        ModelCrudViewSet):
    serializer_class = serializers.ProductIncrementSerializer
    permission_classes = (permissions.ProductIncrementPermission,)
    # filter_backends = (filters.CanViewProductIncrementsFilterBackend,)
    # filter_fields = ("project", "closed")
    queryset = models.ProductIncrement.objects.all()

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        self._add_taiga_info_headers()
        return res

    def _add_taiga_info_headers(self):
        try:
            project_id = int(self.request.QUERY_PARAMS.get("project", None))
            project_model = apps.get_model("projects", "Project")
            project = get_object_or_none(project_model, id=project_id)
        except TypeError:
            project = None

        if project:
            opened_productincrements = project.productincrements.filter(closed=False).count()
            closed_productincrements = project.productincrements.filter(closed=True).count()

            self.headers["Taiga-Info-Total-Opened-ProductIncrements"] = opened_productincrements
            self.headers["Taiga-Info-Total-Closed-ProductIncrements"] = closed_productincrements

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = self.attach_watchers_attrs_to_queryset(qs)
        # qs = qs.prefetch_related("user_stories",
        #                          "user_stories__role_points",
        #                          "user_stories__role_points__points",
        #                          "user_stories__role_points__role",
        #                          "user_stories__generated_from_issue",
        #                          "user_stories__project")
        qs = qs.select_related("project")
        qs = qs.order_by("-created_date")
        return qs

    def pre_save(self, obj):
        if not obj.id:
            obj.owner = self.request.user

        super().pre_save(obj)

    @detail_route(methods=['get'])
    def stats(self, request, pk=None):
        productincrement = get_object_or_404(models.ProductIncrement, pk=pk)

        self.check_permissions(request, "stats", productincrement)

        total_points = productincrement.total_points
        productincrement_stats = {
            'name': productincrement.name,
            # 'estimated_start': productincrement.estimated_start,
            # 'estimated_finish': productincrement.estimated_finish,
            # 'total_points': total_points,
            # 'completed_points': productincrement.closed_points.values(),
            # 'total_userstories': productincrement.user_stories.count(),
            # 'completed_userstories': len([us for us in productincrement.user_stories.all() if us.is_closed]),
            # 'total_tasks': productincrement.tasks.all().count(),
            # 'completed_tasks': productincrement.tasks.all().filter(status__is_closed=True).count(),
            # 'iocaine_doses': productincrement.tasks.filter(is_iocaine=True).count(),
            'days': []
        }
        # current_date = productincrement.estimated_start
        # sumTotalPoints = sum(total_points.values())
        # optimal_points = sumTotalPoints
        # productincrement_days = (productincrement.estimated_finish - productincrement.estimated_start).days
        # optimal_points_per_day = sumTotalPoints / productincrement_days if productincrement_days else 0
        # while current_date <= productincrement.estimated_finish:
        #     productincrement_stats['days'].append({
        #         'day': current_date,
        #         'name': current_date.day,
        #         'open_points':  sumTotalPoints - sum(productincrement.closed_points_by_date(current_date).values()),
        #         'optimal_points': optimal_points,
        #     })
        #     current_date = current_date + datetime.timedelta(days=1)
        #     optimal_points -= optimal_points_per_day

        return response.Ok(productincrement_stats)


class ProductIncrementWatchersViewSet(WatchersViewSetMixin, ModelListViewSet):
    permission_classes = (permissions.ProductIncrementWatchersPermission,)
    resource_model = models.ProductIncrement


class ProductIncrementAttachmentViewSet(BaseAttachmentViewSet):
    permission_classes = (permissions.ProductIncrementAttachmentPermission,)
    # filter_backends = (filters.CanViewProductIncrementAttachmentFilterBackend,)
    content_type = "productships.productincrement"
