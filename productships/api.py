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

from django.utils.translation import ugettext as _
from django.db.models import Q
from django.http import HttpResponse

from taiga.base import filters
from taiga.base import exceptions as exc
from taiga.base import response
from taiga.base.decorators import detail_route, list_route
from taiga.base.api import ModelCrudViewSet, ModelListViewSet
from taiga.base.api.utils import get_object_or_404

from taiga.users.models import User

from taiga.projects.notifications.mixins import WatchedResourceMixin, WatchersViewSetMixin
from taiga.projects.occ import OCCResourceMixin
from taiga.projects.history.mixins import HistoryResourceMixin

from taiga.projects.models import Project, IssueStatus, Severity, Priority, IssueType
from taiga.projects.milestones.models import Milestone
from taiga.projects.votes.mixins.viewsets import VotedResourceMixin, VotersViewSetMixin
from taiga.projects.attachments.api import BaseAttachmentViewSet


from . import models
from . import permissions
from . import serializers
from . import services



class CanViewProductIncrementsFilterBackend(filters.PermissionBasedFilterBackend):
    permission = "view_productincrements"




class ProductIncrementViewSet(OCCResourceMixin, VotedResourceMixin, HistoryResourceMixin, WatchedResourceMixin,
                   ModelCrudViewSet):
    queryset = models.ProductIncrement.objects.all()
    permission_classes = (permissions.ProductIncrementPermission, )
    filter_backends = (CanViewProductIncrementsFilterBackend,
                       filters.OwnersFilter,
                       filters.TagsFilter,
                       filters.WatchersFilter,
                       filters.QFilter,
                       filters.OrderByFilterMixin)
    retrieve_exclude_filters = (filters.OwnersFilter,
                                filters.TagsFilter,
                                filters.WatchersFilter,)

    filter_fields = ("project",
                     "reviewed")

    order_by_fields = (
                       "created_date",
                       "modified_date",
                       "owner",
                       "name",
                       "total_voters")

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["retrieve", "by_ref"]:
            return serializers.ProductIncrementNeighborsSerializer

        if self.action == "list":
            return serializers.ProductIncrementListSerializer

        return serializers.ProductIncrementSerializer

    def update(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()
        project_id = request.DATA.get('project', None)
        if project_id and self.object and self.object.project.id != project_id:
            try:
                new_project = Project.objects.get(pk=project_id)
                self.check_permissions(request, "destroy", self.object)
                self.check_permissions(request, "create", new_project)

                sprint_id = request.DATA.get('milestone', None)
                if sprint_id is not None and new_project.milestones.filter(pk=sprint_id).count() == 0:
                    request.DATA['milestone'] = None
            except Project.DoesNotExist:
                return response.BadRequest(_("The project doesn't exist"))
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("attachments")
        qs = qs.select_related("owner", "project")
        qs = self.attach_votes_attrs_to_queryset(qs)
        return self.attach_watchers_attrs_to_queryset(qs)

    def pre_save(self, obj):
        if not obj.id:
            obj.owner = self.request.user
        super().pre_save(obj)

    def pre_conditions_on_save(self, obj):
        super().pre_conditions_on_save(obj)
        if obj.milestone and obj.milestone.project != obj.project:
            raise exc.PermissionDenied(_("You don't have permissions to set this sprint "
                                         "to this product increment."))

    @list_route(methods=["GET"])
    def by_ref(self, request):
        ref = request.QUERY_PARAMS.get("ref", None)
        project_id = request.QUERY_PARAMS.get("project", None)
        issue = get_object_or_404(models.ProductIncrement, ref=ref, project_id=project_id)
        return self.retrieve(request, pk=issue.pk)

    @list_route(methods=["GET"])
    def filters_data(self, request, *args, **kwargs):
        project_id = request.QUERY_PARAMS.get("project", None)
        project = get_object_or_404(Project, id=project_id)

        filter_backends = self.get_filter_backends()
        owners_filter_backends = (f for f in filter_backends if f != filters.OwnersFilter)
        tags_filter_backends = (f for f in filter_backends if f != filters.TagsFilter)

        queryset = self.get_queryset()
        querysets = {
            "owners": self.filter_queryset(queryset, filter_backends=owners_filter_backends),
            "tags": self.filter_queryset(queryset)
        }
        return response.Ok(services.get_product_increment_filters_data(project, querysets))

    @list_route(methods=["GET"])
    def csv(self, request):
        uuid = request.QUERY_PARAMS.get("uuid", None)
        if uuid is None:
            return response.NotFound()

        project = get_object_or_404(Project, issues_csv_uuid=uuid)
        queryset = project.issues.all().order_by('ref')
        data = services.issues_to_csv(project, queryset)
        csv_response = HttpResponse(data.getvalue(), content_type='application/csv; charset=utf-8')
        csv_response['Content-Disposition'] = 'attachment; filename="productincrements.csv"'
        return csv_response

    @list_route(methods=["POST"])
    def bulk_create(self, request, **kwargs):
        serializer = serializers.IssuesBulkSerializer(data=request.DATA)
        if serializer.is_valid():
            data = serializer.data
            project = Project.objects.get(pk=data["project_id"])
            self.check_permissions(request, 'bulk_create', project)
            issues = services.create_issues_in_bulk(
                data["bulk_issues"], project=project, owner=request.user,
                status=project.default_issue_status, severity=project.default_severity,
                priority=project.default_priority, type=project.default_issue_type,
                callback=self.post_save, precall=self.pre_save)
            issues_serialized = self.get_serializer_class()(issues, many=True)

            return response.Ok(data=issues_serialized.data)

        return response.BadRequest(serializer.errors)


class ProductIncrementVotersViewSet(VotersViewSetMixin, ModelListViewSet):
    permission_classes = (permissions.ProductIncrementVotersPermission,)
    resource_model = models.ProductIncrement


class ProductIncrementWatchersViewSet(WatchersViewSetMixin, ModelListViewSet):
    permission_classes = (permissions.ProductIncrementWatchersPermission,)
    resource_model = models.ProductIncrement

# Adding here also the corresponding attachment viewset

class ProductIncrementAttachmentViewSet(BaseAttachmentViewSet):
    permission_classes = (permissions.ProductIncrementAttachmentPermission,)
    #filter_backends = (filters.CanViewProductIncrementAttachmentFilterBackend,)
    content_type = "productincrements.productincrement"