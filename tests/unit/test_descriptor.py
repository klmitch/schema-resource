# Copyright (C) 2019 by Kevin L. Mitchell <klmitch@mit.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

from six.moves.urllib import parse as urlparse

from schema_res import descriptor


class TestSchemaDescriptor(object):
    def test_init(self):
        result = descriptor.SchemaDescriptor('file.yaml')

        assert result.uri == urlparse.urlparse('file.yaml')
        assert result.schema is None

    def test_get_cached(self, mocker):
        mock_load_schema = mocker.patch.object(
            descriptor.loader, 'load_schema',
        )
        owner = mocker.Mock(__module__='pkg')
        obj = descriptor.SchemaDescriptor('file.yaml')
        obj.schema = 'schema'

        result = obj.__get__(None, owner)

        assert result == 'schema'
        assert obj.schema == 'schema'
        mock_load_schema.assert_not_called()

    def test_get_absolute(self, mocker):
        mock_load_schema = mocker.patch.object(
            descriptor.loader, 'load_schema',
        )
        owner = mocker.Mock(__module__='pkg')
        obj = descriptor.SchemaDescriptor('res://abs/file.yaml#frag')

        result = obj.__get__(None, owner)

        assert result == mock_load_schema.return_value
        assert obj.schema == mock_load_schema.return_value
        mock_load_schema.assert_called_once_with('res://abs/file.yaml#frag')

    def test_get_relative(self, mocker):
        mock_load_schema = mocker.patch.object(
            descriptor.loader, 'load_schema',
        )
        owner = mocker.Mock(__module__='pkg')
        obj = descriptor.SchemaDescriptor('file.yaml#frag')

        result = obj.__get__(None, owner)

        assert result == mock_load_schema.return_value
        assert obj.schema == mock_load_schema.return_value
        mock_load_schema.assert_called_once_with('res://pkg/file.yaml#frag')
