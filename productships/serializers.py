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

import json
from taiga.base.api import serializers

from taiga.base.fields import TagsField, JsonField
from taiga.base.fields import PgArrayField

from taiga.base.neighbors import NeighborsSerializerMixin

from taiga.mdrender.service import render as mdrender
from taiga.projects.validators import ProjectExistsValidator
from taiga.projects.milestones.validators import SprintExistsValidator
from taiga.projects.tasks.validators import TaskExistsValidator
from taiga.projects.notifications.validators import WatchersValidator
from taiga.projects.serializers import BasicTaskStatusSerializerSerializer
from taiga.projects.notifications.mixins import EditableWatchedResourceModelSerializer
from taiga.projects.votes.mixins.serializers import VoteResourceSerializerMixin

from taiga.users.serializers import UserBasicInfoSerializer

from . import models


class ProductIncrementSerializer(WatchersValidator, VoteResourceSerializerMixin, EditableWatchedResourceModelSerializer,
                                 serializers.ModelSerializer):
    tags = TagsField(required=False)
    external_reference = PgArrayField(required=False)
    reviewed = serializers.Field(source="reviewed")
    comment = serializers.SerializerMethodField("get_comment")
    # generated_user_stories = serializers.SerializerMethodField("get_generated_user_stories")
    description_html = serializers.SerializerMethodField("get_description_html")
    owner_extra_info = UserBasicInfoSerializer(source="owner", required=False, read_only=True)

    class Meta:
        model = models.ProductIncrement
        read_only_fields = ('id', 'ref', 'created_date', 'modified_date')

    def get_comment(self, obj):
        # NOTE: This method and field is necessary to historical comments work
        return ""

    def get_description_html(self, obj):
        return mdrender(obj.project, obj.description)


class ProductIncrementNeighborsSerializer(NeighborsSerializerMixin, ProductIncrementSerializer):
    def serialize_neighbor(self, neighbor):
        return NeighborProductIncrementSerializer(neighbor).data


class NeighborProductIncrementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductIncrement
        fields = ("id", "ref", "name")
        depth = 0


class ProductIncrementListSerializer(ProductIncrementSerializer):
    class Meta:
        model = models.ProductIncrement
        read_only_fields = ('id', 'ref', 'created_date', 'modified_date')
        exclude = ("description", "description_html")


class MarkerSerializer(serializers.ModelSerializer):

    data = serializers.SerializerMethodField("get_data")
    marker_json = JsonField()

    class Meta:
        model = models.MediaMarker
        read_only_fields = ('id', 'created_date', 'modified_date')
        exclude = ("marker_json", )

    def get_data(self, obj):
        return obj.marker_json
