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

from django.contrib import admin

from taiga.projects.notifications.admin import WatchedInline
from taiga.projects.votes.admin import VoteInline


from . import models


# class ProductIncrementAdmin(admin.ModelAdmin):
#     list_display = ["id", "name", "project"]
#     list_display_links = ["id", "name"]
#     inlines = [WatchedInline, VoteInline]
#     raw_id_fields = ["project"]
#     search_fields = ["description", "id", ]

    # def get_object(self, *args, **kwargs):
    #     self.obj = super().get_object(*args, **kwargs)
    #     return self.obj
    #
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if (db_field.name in ["status", "milestone", "user_story"]
    #             and getattr(self, 'obj', None)):
    #         kwargs["queryset"] = db_field.related.model.objects.filter(
    #                                                   project=self.obj.project)
    #     elif (db_field.name in ["owner", "assigned_to"]
    #             and getattr(self, 'obj', None)):
    #         kwargs["queryset"] = db_field.related.model.objects.filter(
    #                                      memberships__project=self.obj.project)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
    #
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if (db_field.name in ["watchers"]
    #             and getattr(self, 'obj', None)):
    #         kwargs["queryset"] = db_field.related.parent_model.objects.filter(
    #                                      memberships__project=self.obj.project)
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)

class ProductIncrementAdmin(admin.ModelAdmin):
    list_display = ["id","name", "reviewed", "project",]
    list_display_links = ["id","name"]
    search_fields = ["id", "attachments", "project__name", "project__slug"]
    raw_id_fields = ["project"]
    inlines = [WatchedInline, VoteInline]

    def get_object(self, *args, **kwargs):
        self.obj = super().get_object(*args, **kwargs)
        return self.obj

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name in ["milestone"]
                and getattr(self, 'obj', None)):
            kwargs["queryset"] = db_field.related.model.objects.filter(
                                                      project=self.obj.project)
        elif (db_field.name in ["owner"]
                and getattr(self, 'obj', None)):
            kwargs["queryset"] = db_field.related.model.objects.filter(
                                         memberships__project=self.obj.project)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if (db_field.name in ["watchers"]
                and getattr(self, 'obj', None)):
            kwargs["queryset"] = db_field.related.parent_model.objects.filter(
                                         memberships__project=self.obj.project)
        return super().formfield_for_manytomany(db_field, request, **kwargs)



class MediaMarkerAdmin(admin.ModelAdmin):
    list_display = ["id","attachment", "created_date", "modified_date", "owner",]
    list_display_links = ["id", "attachment",]
    search_fields = ["marker_content",]
    #raw_id_fields = ["project"]


admin.site.register(models.ProductIncrement, ProductIncrementAdmin)
admin.site.register(models.MediaMarker, MediaMarkerAdmin)



