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

import pytest

from schema_res import loader


class TestResHandler(object):
    def test_base(self, mocker):
        mock_resource_stream = mocker.patch.object(
            loader.pkg_resources, 'resource_stream', mocker.mock_open(),
        )
        mock_safe_load = mocker.patch.object(loader.yaml, 'safe_load')

        result = loader._res_handler('res://pkg/res.yaml')

        assert result == mock_safe_load.return_value
        mock_resource_stream.assert_called_once_with('pkg', 'res.yaml')
        mock_safe_load.assert_called_once_with(
            mock_resource_stream.return_value,
        )

    def test_bad_scheme(self, mocker):
        mock_resource_stream = mocker.patch.object(
            loader.pkg_resources, 'resource_stream', mocker.mock_open(),
        )
        mock_safe_load = mocker.patch.object(loader.yaml, 'safe_load')

        with pytest.raises(ValueError):
            loader._res_handler('bad://pkg/res.yaml')
        mock_resource_stream.assert_not_called()
        mock_safe_load.assert_not_called()

    def test_no_netloc(self, mocker):
        mock_resource_stream = mocker.patch.object(
            loader.pkg_resources, 'resource_stream', mocker.mock_open(),
        )
        mock_safe_load = mocker.patch.object(loader.yaml, 'safe_load')

        with pytest.raises(ValueError):
            loader._res_handler('res:///res.yaml')
        mock_resource_stream.assert_not_called()
        mock_safe_load.assert_not_called()

    def test_slash_path(self, mocker):
        mock_resource_stream = mocker.patch.object(
            loader.pkg_resources, 'resource_stream', mocker.mock_open(),
        )
        mock_safe_load = mocker.patch.object(loader.yaml, 'safe_load')

        with pytest.raises(ValueError):
            loader._res_handler('res://pkg/')
        mock_resource_stream.assert_not_called()
        mock_safe_load.assert_not_called()

    def test_no_path(self, mocker):
        mock_resource_stream = mocker.patch.object(
            loader.pkg_resources, 'resource_stream', mocker.mock_open(),
        )
        mock_safe_load = mocker.patch.object(loader.yaml, 'safe_load')

        with pytest.raises(ValueError):
            loader._res_handler('res://pkg')
        mock_resource_stream.assert_not_called()
        mock_safe_load.assert_not_called()


class TestLoadSchema(object):
    def test_base(self, mocker):
        mock_res_handler = mocker.patch.object(loader, '_res_handler')
        sch = mock_res_handler.return_value
        mock_RefResolver = mocker.patch.object(
            loader.jsonschema, 'RefResolver',
        )
        resolver = mock_RefResolver.return_value
        mock_validator_for = mocker.patch.object(
            loader.jsonschema.validators, 'validator_for',
        )
        val = mock_validator_for.return_value

        result = loader.load_schema('uri')

        assert result == val.return_value
        mock_res_handler.assert_called_once_with('uri')
        mock_RefResolver.assert_called_once_with(
            'uri', sch,
            handlers={'res': loader._res_handler},
        )
        mock_validator_for.assert_called_once_with(sch)
        val.check_schema.assert_not_called()
        val.assert_called_once_with(sch, resolver=resolver)

    def test_validate(self, mocker):
        mock_res_handler = mocker.patch.object(loader, '_res_handler')
        sch = mock_res_handler.return_value
        mock_RefResolver = mocker.patch.object(
            loader.jsonschema, 'RefResolver',
        )
        resolver = mock_RefResolver.return_value
        mock_validator_for = mocker.patch.object(
            loader.jsonschema.validators, 'validator_for',
        )
        val = mock_validator_for.return_value

        result = loader.load_schema('uri', True)

        assert result == val.return_value
        mock_res_handler.assert_called_once_with('uri')
        mock_RefResolver.assert_called_once_with(
            'uri', sch,
            handlers={'res': loader._res_handler},
        )
        mock_validator_for.assert_called_once_with(sch)
        val.check_schema.assert_called_once_with(sch)
        val.assert_called_once_with(sch, resolver=resolver)
