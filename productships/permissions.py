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

from taiga.base.api.permissions import (TaigaResourcePermission, HasProjectPerm,PermissionComponent,
                                        IsAuthenticated, IsProjectOwner, AllowAny,
                                        IsSuperUser)
from taiga.projects.attachments.permissions import IsAttachmentOwnerPerm


class ProductIncrementPermission(TaigaResourcePermission):
    enought_perms = IsProjectOwner() | IsSuperUser()
    global_perms = None
    retrieve_perms = HasProjectPerm('view_productsincrements')
    create_perms = HasProjectPerm('add_productsincrement')
    update_perms = HasProjectPerm('modify_productsincrement')
    partial_update_perms = HasProjectPerm('modify_productsincrement')
    destroy_perms = HasProjectPerm('delete_productsincrement')
    list_perms = AllowAny()
    stats_perms = HasProjectPerm('view_productsincrements')
    watch_perms = IsAuthenticated() & HasProjectPerm('view_productsincrements')
    unwatch_perms = IsAuthenticated() & HasProjectPerm('view_productsincrements')


class ProductIncrementWatchersPermission(TaigaResourcePermission):
    enought_perms = IsProjectOwner() | IsSuperUser()
    global_perms = None
    retrieve_perms = HasProjectPerm('view_productsincrements')
    list_perms = HasProjectPerm('view_productsincrements')


class ProductIncrementAttachmentPermission(TaigaResourcePermission):
    retrieve_perms = HasProjectPerm('view_productincrement') | IsAttachmentOwnerPerm()
    create_perms = HasProjectPerm('modify_productincrement')
    update_perms = HasProjectPerm('modify_productincrement') | IsAttachmentOwnerPerm()
    partial_update_perms = HasProjectPerm('modify_productincrement') | IsAttachmentOwnerPerm()
    destroy_perms = HasProjectPerm('modify_productincrement') | IsAttachmentOwnerPerm()
    list_perms = AllowAny()

class HasProductIncrementIdUrlParam(PermissionComponent):
    def check_permissions(self, request, view, obj=None):
        param = view.kwargs.get('product_increment_id', None)
        if param:
            return True
        return False


class ProductIncrementVotersPermission(TaigaResourcePermission):
    enought_perms = IsProjectOwner() | IsSuperUser()
    global_perms = None
    retrieve_perms = HasProjectPerm('view_product_increments')



class ProductIncrementAttachmentPermission(TaigaResourcePermission):
    retrieve_perms = HasProjectPerm('view_pi') | IsAttachmentOwnerPerm()
    create_perms = HasProjectPerm('modify_pi')
    update_perms = HasProjectPerm('modify_pi') | IsAttachmentOwnerPerm()
    partial_update_perms = HasProjectPerm('modify_pi') | IsAttachmentOwnerPerm()
    destroy_perms = HasProjectPerm('modify_pi') | IsAttachmentOwnerPerm()
    list_perms = AllowAny()