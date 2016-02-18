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

from collections import OrderedDict


def _get_productincrements_owners(project, queryset):
    compiler = connection.ops.compiler(queryset.query.compiler)(queryset.query, connection, None)
    queryset_where_tuple = queryset.query.where.as_sql(compiler, connection)
    where = queryset_where_tuple[0]
    where_params = queryset_where_tuple[1]

    extra_sql = """
        WITH counters AS (
        	SELECT "productincrements_productincrement"."owner_id" owner_id,
        	count("productincrements_productincrement"."owner_id") count
        		FROM "productincrements_productincrement"
        		INNER JOIN "projects_project"
        		ON ("productincrements_productincrement"."project_id" = "projects_project"."id")
			    WHERE {where}
        		GROUP BY "productincrements_productincrement"."owner_id"
               )
        SELECT
        	"projects_membership"."user_id" id,
        	"users_user"."full_name",
        	COALESCE("counters".count, 0) count
        FROM projects_membership
        LEFT OUTER JOIN counters ON ("projects_membership"."user_id" = "counters"."owner_id")
        INNER JOIN "users_user" ON ("projects_membership"."user_id" = "users_user"."id")
        WHERE ("projects_membership"."project_id" = %s AND "projects_membership"."user_id" IS NOT NULL)

        -- System users
        UNION
    		SELECT
    			"users_user"."id" user_id,
    			"users_user"."full_name" full_name,
    			COALESCE("counters".count, 0) count
    		FROM users_user
    		LEFT OUTER JOIN counters ON ("users_user"."id" = "counters"."owner_id")
    		WHERE ("users_user"."is_system" IS TRUE)
    """.format(where=where)

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, where_params + [project.id])
        rows = cursor.fetchall()

    result = []
    for id, full_name, count in rows:
        if count > 0:
            result.append({
                "id": id,
                "full_name": full_name,
                "count": count,
            })
    return sorted(result, key=itemgetter("full_name"))


def _get_productincrements_tags(queryset):
    tags = []
    for t_list in queryset.values_list("tags", flat=True):
        if t_list is None:
            continue
        tags += list(t_list)

    tags = [{"name":e, "count":tags.count(e)} for e in set(tags)]

    return sorted(tags, key=itemgetter("name"))


def get_product_increment_filters_data(project, querysets):
    """
    Given a project and an issues queryset, return a simple data structure
    of all possible filters for the issues in the queryset.
    """
    data = OrderedDict([
        ("owners", _get_productincrements_owners(project, querysets["owners"])),
        ("tags", _get_productincrements_tags(querysets["tags"])),
    ])

    return data
