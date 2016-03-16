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


import os
import os.path as path
from unidecode import unidecode

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _
from django.utils.text import get_valid_filename

from django_pgjson.fields import JsonField
from taiga.projects.occ.mixins import OCCModelMixin
from taiga.projects.notifications.mixins import WatchedModelMixin
from taiga.base.tags import TaggedMixin
from djorm_pgarray.fields import TextArrayField


class ProductIncrement(OCCModelMixin, WatchedModelMixin, TaggedMixin, models.Model):
    """
    Potetially Shippable Product Increment - Drops and / or demos to the customer
    """
    ref = models.BigIntegerField(db_index=True, null=True, blank=True, default=None,
                                 verbose_name=_("ref"))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                              related_name="change_product_increments",
                              verbose_name=_("owner"))
    project = models.ForeignKey("projects.Project", null=False, blank=False,
                                related_name="product_increments", verbose_name=_("project"))
    created_date = models.DateTimeField(null=False, blank=False,
                                        verbose_name=_("created date"),
                                        default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False,
                                         verbose_name=_("modified date"))
    name = models.CharField(blank=True, default="", max_length=500)
    milestone = models.ForeignKey("milestones.Milestone", null=True, blank=True,
                                  default=None, related_name="product_increments",
                                  verbose_name=_("milestone"))
    attachments = generic.GenericRelation("attachments.Attachment")
    reviewed = models.BooleanField(default=False, verbose_name=_("reviewed"))
    description = models.TextField(null=False, blank=True, verbose_name=_("description"))
    order = models.IntegerField(default=0, null=False, blank=False, verbose_name=_("order"))
    external_reference = TextArrayField(default=None, verbose_name=_("external reference"))
    _importing = None

    class Meta:
        verbose_name = "product_increment"
        verbose_name_plural = "product_increments"
        ordering = ["project", "created_date", "-id"]
        permissions = (
            ("view_productincrement", "Can view product increments"),
        )

    def save(self, *args, **kwargs):
        if not self._importing or not self.modified_date:
            self.modified_date = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Product Increment: {}".format(self.id)


class MediaMarker(models.Model):
    """
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                              related_name="change_media_markers",
                              verbose_name=_("owner"))

    attachment = models.ForeignKey("attachments.Attachment", null=False, blank=False,
                                   related_name="markers", verbose_name=_("Product Increment"))
    created_date = models.DateTimeField(null=False, blank=False,
                                        verbose_name=_("created date"),
                                        default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False,
                                         verbose_name=_("modified date"))
    marker_content = models.TextField(null=False, blank=True, verbose_name=_("marker_content"))
    marker_json = JsonField(null=True, blank=True)

    class Meta:
        verbose_name = "media_marker"
        verbose_name_plural = "media_markers"
        ordering = ["created_date", "id"]
        permissions = (
            ("view_media_marker", "Can view media marker"),
        )
