# -*- coding: utf8 -*-

# Copyright (C) 2014-2016 Ben Ockmore, Stanisław Szcześniak

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module specifies a class, Resource, which is designed to be used as the
base class for all resource models specified in this package."""

from base import Base
from simple_objects import Alias, Identifier, Relationship, \
    Disambiguation, Annotation
from revision import Revision

class Entity(Base):
    """Resource class, from which all other resource models are derived."""
    def __init__(self):
        super(self.__class__, self).__init__()
        self.entity_gid = None
        self.uri = None
        self.type = None

        self.last_updated = None

        self.annotation = None
        self.annotation_uri = None

        self.disambiguation = None
        self.disambiguation_uri = None

        self.default_alias = None
        self.aliases = None
        self.aliases_uri = None

        self.identifiers = None
        self.identifiers_uri = None

        self.relationships = None
        self.relationships_uri = None

        self.revision = None

    def fetch_from_json(self, json_data):
        self.entity_gid = json_data['entity_gid']
        self.uri = json_data['uri']
        self.type = json_data['_type']

        self.last_updated = json_data['last_updated']
        self.default_alias = Alias.from_json(json_data['default_alias'])

        if 'aliases' in json_data:
            self.aliases = aliases_from_json(json_data['aliases'])

        if 'relationships' in json_data:
            self.relationships = \
                relationships_from_json(json_data['relationships'])

        if 'identifiers' in json_data:
            self.identifiers = identifiers_from_json(json_data['identifiers'])

        if 'annotation' in json_data:
            self.annotation = Annotation.from_json(json_data['annotation'])

        if 'disambiguation' in json_data:
            self.disambiguation = \
                Disambiguation.from_json(json_data['disambiguation'])

        self.revision = Revision.from_json(json_data['revision'])


def aliases_from_json(json_data):
    return [Alias.from_json(alias) for alias in json_data['objects']]


def identifiers_from_json(json_data):
    return [Identifier.from_json(id) for id in json_data['objects']]


def relationships_from_json(json_data):
    return [Relationship.from_json(rel) for rel in json_data['objects']]


def format_date(date, precision):
    if date is None:
        return None

    if precision == 'YEAR':
        return '{:02}'.format(date.year)
    elif precision == 'MONTH':
        return '{:02}-{:02}'.format(date.year, date.month)
    else:
        return '{:02}-{:02}-{:02}'.format(date.year, date.month, date.day)
